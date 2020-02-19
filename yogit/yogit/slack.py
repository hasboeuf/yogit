"""
Slack API requester
"""
import click

from urllib.parse import urlparse

from yogit.yogit.settings import Settings
from yogit.api.requester import http_call
from yogit.utils.spinner import spin
from yogit.yogit.logger import LOGGER

SLACK_API_URL = "https://slack.com/api"
SLACK_POST_MESSAGE_ENDPOINT = "/chat.postMessage"
SLACK_AUTH_CHECK_ENDPOINT = "/auth.test"
SLACK_CHANNEL_LIST_ENDPOINT = "/conversations.list"
SLACK_MESSAGE_LINK_ENDPOINT = "/chat.getPermalink"


def _get_slack_url(endpoint):
    return SLACK_API_URL + endpoint


def _get_headers():
    """
    Craft HTTP headers for request
    """
    return {"Content-Type": "application/x-www-form-urlencoded"}


class SlackRESTClient:
    """
    Slack REST API client
    """

    def post(self, endpoint, payload):
        """
        Perform POST Slack REST request
        """
        url = _get_slack_url(endpoint)
        LOGGER.debug("POST %s", url)
        LOGGER.debug(payload)
        return http_call("post", url, data=payload)

    def get(self, endpoint, params):
        """
        Perform GET Slack REST request
        """
        settings = Settings()
        url = _get_slack_url(endpoint)
        LOGGER.debug("GET %s", url)
        params.append(("token", settings.get_slack_token()))
        return http_call("get", url, headers=_get_headers(), params=params)


class SlackQuery:
    """
    Represent a Slack query
    """

    def __init__(self, method, endpoint, params=[]):
        self.response = None
        self.client = SlackRESTClient()
        self.method = method
        self.endpoint = endpoint
        self.params = params
        self.payload = {}

    def _handle_response(self, response):
        raise NotImplementedError()

    @spin
    def execute(self, spinner):
        """ Execute the query """
        if self.method == "post":
            response = self.client.post(self.endpoint, self.payload)
        else:
            response = self.client.get(self.endpoint, self.params)
        if not response.get("ok", False):
            raise click.ClickException("Slack API: {}".format(response.get("error", "default_error")))
        self._handle_response(response)


class SlackAuthCheck(SlackQuery):
    """
    Check auth token
    """

    def __init__(self):
        super().__init__("post", SLACK_AUTH_CHECK_ENDPOINT)
        settings = Settings()
        self.user = None
        self.payload = {"token": settings.get_slack_token()}

    def _handle_response(self, response):
        try:
            self.user = response["user"]
        except KeyError as error:
            raise click.ClickException("Bad response")


class SlackPostMessageQuery(SlackQuery):
    """
    Post a message or a reply
    """

    def __init__(self, message, reply_to=None):
        super().__init__("post", SLACK_POST_MESSAGE_ENDPOINT)
        self.message = message
        self.reply_to = reply_to
        self.ts = None
        self.channel_id = None
        self.payload = self._get_payload()

    def _get_payload(self):
        settings = Settings()
        payload = {
            "token": settings.get_slack_token(),
            "channel": settings.get_slack_channel(),
            "text": self.message,
            "as_user": True,
            "link_names": True,
        }
        if self.reply_to is not None:
            payload.update({"thread_ts": self.reply_to.ts})
        return payload

    def _handle_response(self, response):
        self.ts = response.get("ts")
        self.channel_id = response.get("channel")


class SlackChannelListQuery(SlackQuery):
    """
    Request Slack channel list
    """

    def __init__(self):
        super().__init__("get", SLACK_CHANNEL_LIST_ENDPOINT, params=[("limit", 1000)])
        self.channels = []

    def _handle_response(self, response):
        self.channels = [x["name"] for x in response["channels"]]


class SlackMessageLinkQuery(SlackQuery):
    """
    Get Slack url of a message
    """

    def __init__(self, link_of):
        super().__init__(
            "get", SLACK_MESSAGE_LINK_ENDPOINT, params=[("channel", link_of.channel_id), ("message_ts", link_of.ts)]
        )
        self.url = None

    def _handle_response(self, response):
        self.url = response.get("permalink")
