from unittest.mock import Mock
import responses
import pytest
from click.testing import CliRunner

from yogit.yogit import cli
from yogit.yogit.settings import Settings
from yogit.yogit.errors import ExitCode
from yogit.yogit.account import get_welcome_text
from yogit.api.client import GITHUB_API_URL_V4, GITHUB_API_URL_V3
from yogit.tests.mocks.mock_settings import temporary_settings, mock_settings, assert_empty_settings


def _add_graphql_response(status, json):
    responses.add(responses.POST, GITHUB_API_URL_V4, json=json, status=status)


def _add_rest_response(endpoint, status, json):
    responses.add(responses.GET, GITHUB_API_URL_V3 + endpoint, json=json, status=status)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_setup_erase_settings(runner):
    _add_graphql_response(401, {})
    result = runner.invoke(cli.main, ["account", "setup"], input="<bad_token>")
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == get_welcome_text() + ("\nGitHub token: \n" "Error: Unauthorized\n")
    assert_empty_settings()


@pytest.mark.usefixtures("temporary_settings")
@responses.activate
def test_setup_ok(runner):
    _add_graphql_response(200, {"data": {"viewer": {"login": "user1"}}})
    _add_rest_response("/user/emails", 200, [{"email": "email1"}, {"email": "email2"}, {"email": "email3"}])
    result = runner.invoke(cli.main, ["account", "setup"], input="<token>")
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == get_welcome_text() + ("\nGitHub token: \n" "Hello user1!\n")
    settings = Settings()
    assert settings.get_token() == "<token>"
    assert settings.get_login() == "user1"
    assert settings.get_emails() == ["email1", "email2", "email3"]


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_ratelimit_ok(runner):
    _add_graphql_response(
        200, {"data": {"rateLimit": {"limit": 5000, "cost": 1, "remaining": 4000, "resetAt": "2019-07-11T23:39:39Z"}}}
    )
    result = runner.invoke(cli.main, ["account", "usage"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == "4000/5000 until 2019-07-11T23:39:39Z\n"
