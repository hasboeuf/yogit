import click
import responses
import pytest

from yogit.api.client import RESTClient, GITHUB_API_URL_V3


def _add_response(status, json):
    responses.add(responses.GET, GITHUB_API_URL_V3 + "/endpoint", json=json, status=status)


@responses.activate
def test_ok_200():
    _add_response(200, {"data": "result"})
    client = RESTClient()

    assert client.get("/endpoint") == {"data": "result"}


@responses.activate
def test_ko_400():
    _add_response(400, {"error": "result"})
    client = RESTClient()
    with pytest.raises(click.ClickException) as e:
        client.get("/endpoint")

    assert str(e.value) == "Bad request"


@responses.activate
def test_ko_401():
    _add_response(401, {"error": "result"})
    client = RESTClient()
    with pytest.raises(click.ClickException) as e:
        client.get("/endpoint")

    assert str(e.value) == "Unauthorized"


@responses.activate
def test_ko():
    _add_response(500, {"error": "result"})
    client = RESTClient()
    with pytest.raises(click.ClickException) as e:
        client.get("/endpoint")

    assert str(e.value) == '{"error": "result"}'
