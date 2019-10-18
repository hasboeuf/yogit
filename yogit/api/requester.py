import requests

import click
from requests_toolbelt.utils import dump

from yogit.yogit.logger import LOGGER


def http_call(method, url, **kwargs):
    """
    Perform HTTP call

    - Check status code
    - Check JSON validity
    - Return reponse content as a dict
    """
    try:
        response = requests.request(method, url, **kwargs)
        if response:
            LOGGER.info("Response: %s", response.status_code)
        else:
            LOGGER.info("Response: %s", dump.dump_all(response).decode("utf-8"))
    except requests.RequestException as exception:
        LOGGER.error(str(exception))
        raise click.ClickException(str(exception))

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
