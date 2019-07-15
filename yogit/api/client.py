"""
GitHub API requester
"""
import json
import requests

from requests_toolbelt.utils import dump
import click

from yogit.yogit.logger import LOGGER
from yogit.yogit.settings import Settings

GITHUB_API_URL_V4 = "https://api.github.com/graphql"
GITHUB_API_URL_V3 = "https://api.github.com"


def _http_call(method, url, **kwargs):
    """
    Perform HTTP call and log around it
    """
    try:
        response = requests.request(method, url, **kwargs)
        if response:
            LOGGER.info("Response: %s", response.status_code)
        else:
            LOGGER.info("Response: %s", dump.dump_all(response).decode("utf-8"))
        return response
    except requests.RequestException as exception:
        raise click.ClickException(str(exception))


def _get_authorization():
    """
    Craft Authorization HTTP header
    """
    token = Settings().get_token()
    return "token {}".format(token)


def _get_headers():
    """
    Craft HTTP headers for request
    """
    return {"Accept": "application/json", "Content-Type": "application/json", "Authorization": _get_authorization()}


class GraphQLClient:
    """
    GitHub GraphQL API client
    """

    def __init__(self):
        self.url = GITHUB_API_URL_V4

    def get(self, query):
        """
        Perform GET GitHub GraphQL request
        """
        payload = json.dumps({"query": query})
        LOGGER.debug(payload)
        response = _http_call("post", self.url, headers=_get_headers(), data=payload)
        LOGGER.debug(response.content[:500])
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as exception:
                LOGGER.error(str(exception))
                raise click.ClickException(response.text)
        elif response.status_code == 400:
            raise click.ClickException("Bad request")
        elif response.status_code == 401:
            raise click.ClickException("Unauthorized")
        else:
            raise click.ClickException(response.text)


class RESTClient:
    """
    GitHub REST API client
    """

    def _get_url(self, endpoint):
        return GITHUB_API_URL_V3 + endpoint

    def get(self, endpoint):
        """
        Perform GET GitHub REST request
        """
        url = self._get_url(endpoint)
        LOGGER.debug("GET %s", url)
        response = _http_call("get", url, headers=_get_headers())
        LOGGER.debug(response.json())
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as exception:
                LOGGER.error(str(exception))
                raise click.ClickException(response.text)
        elif response.status_code == 400:
            raise click.ClickException("Bad request")
        elif response.status_code == 401:
            raise click.ClickException("Unauthorized")
        else:
            raise click.ClickException(response.text)
