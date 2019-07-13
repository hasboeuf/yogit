import click
import responses
import pytest

from yogit.api.client import GraphQLClient, GITHUB_API_URL_V4


def _add_response(status, json):
    responses.add(responses.POST, GITHUB_API_URL_V4, json=json, status=status)


@responses.activate
def test_ok_200():
    _add_response(200, {"data": "result"})
    client = GraphQLClient()

    assert client.get({"query": "request"}) == {"data": "result"}


@responses.activate
def test_ko_400():
    _add_response(400, {"error": "result"})
    client = GraphQLClient()
    with pytest.raises(click.ClickException) as e:
        client.get({"query": "request"})

    assert str(e.value) == "Bad request"


@responses.activate
def test_ko_401():
    _add_response(401, {"error": "result"})
    client = GraphQLClient()
    with pytest.raises(click.ClickException) as e:
        client.get({"query": "request"})

    assert str(e.value) == "Unauthorized"


@responses.activate
def test_ko():
    _add_response(500, {"error": "result"})
    client = GraphQLClient()
    with pytest.raises(click.ClickException) as e:
        client.get({"query": "request"})

    assert str(e.value) == '{"error": "result"}'
