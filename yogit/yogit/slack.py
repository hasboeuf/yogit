"""
Slack API requester
"""
import click

from yogit.yogit.settings import Settings
from yogit.api.requester import http_call
from yogit.utils.spinner import spin
from yogit.yogit.logger import LOGGER

SLACK_API_URL = "https://slack.com/api"
SLACK_POST_MESSAGE_ENDPOINT = "/chat.postMessage"
SLACK_AUTH_CHECK_ENDPOINT = "/auth.test"


def _get_slack_url(endpoint):
    return SLACK_API_URL + endpoint


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


class SlackQuery:
    """
    Represent a Slack query
    """

    def __init__(self, endpoint):
        self.response = None
        self.client = SlackRESTClient()
        self.endpoint = endpoint
        self.payload = {}

    def _handle_response(self, response):
        raise NotImplementedError()

    @spin
    def execute(self, spinner):
        """ Execute the query """
        response = self.client.post(self.endpoint, self.payload)
        if not response.get("ok", False):
            raise click.ClickException("Slack API: {}".format(response.get("error", "default_error")))
        self._handle_response(response)


class SlackAuthCheck(SlackQuery):
    """
    Check auth token
    """

    def __init__(self):
        super().__init__(SLACK_AUTH_CHECK_ENDPOINT)
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
        super().__init__(SLACK_POST_MESSAGE_ENDPOINT)
        self.message = message
        self.reply_to = reply_to
        self.thread_id = None
        self.payload = self._get_payload()

    def _get_payload(self):
        settings = Settings()
        payload = {
            "token": settings.get_slack_token(),
            "channel": settings.get_slack_channel(),
            "text": self.message,
            "as_user": True,
        }
        if self.reply_to is not None:
            payload.update({"thread_ts": self.reply_to.thread_id})
        return payload

    def _handle_response(self, response):
        self.thread_id = response.get("ts")
