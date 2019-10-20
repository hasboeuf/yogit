from unittest.mock import Mock
import responses
import pytest
from click.testing import CliRunner

from yogit.yogit import cli
from yogit.yogit.settings import Settings
from yogit.yogit.errors import ExitCode
from yogit.yogit.account import get_welcome_text, get_github_text, get_slack_text
from yogit.api.client import GITHUB_API_URL_V4, GITHUB_API_URL_V3
from yogit.yogit.slack import SLACK_API_URL, SLACK_AUTH_CHECK_ENDPOINT, SLACK_CHANNEL_LIST_ENDPOINT
from yogit.tests.mocks.mock_settings import temporary_settings, mock_settings, assert_empty_settings


def _add_graphql_response(status, json):
    responses.add(responses.POST, GITHUB_API_URL_V4, json=json, status=status)


def _add_rest_response(endpoint, status, json):
    responses.add(responses.GET, GITHUB_API_URL_V3 + endpoint, json=json, status=status)


def _add_post_slack_api_response(endpoint, json):
    responses.add(responses.POST, SLACK_API_URL + endpoint, json=json, status=200)


def _add_get_slack_api_response(endpoint, json):
    responses.add(responses.GET, SLACK_API_URL + endpoint, json=json, status=200)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_setup_does_not_erase_if_user_does_not_want(runner):
    result = runner.invoke(cli.main, ["account", "setup"], input="\n".join(["n", "n"]))
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert "Reset GitHub config?" in result.output
    assert "Reset Slack config?" in result.output
    settings = Settings()
    assert settings.is_github_valid()
    assert settings.is_slack_valid()


@pytest.mark.usefixtures("temporary_settings")
@responses.activate
def test_setup_github_unauthorized(runner):
    _add_graphql_response(401, {})
    result = runner.invoke(cli.main, ["account", "setup"], input="bad_token")
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == "\n".join(
        [get_welcome_text(), get_github_text(), "GitHub token: ", "Error: Unauthorized\n"]
    )
    assert_empty_settings()


@pytest.mark.usefixtures("temporary_settings")
@responses.activate
def test_setup_ok(runner):
    _add_graphql_response(200, {"data": {"viewer": {"login": "user1"}}})
    _add_rest_response("/user/emails", 200, [{"email": "email1"}, {"email": "email2"}, {"email": "email3"}])
    _add_post_slack_api_response(SLACK_AUTH_CHECK_ENDPOINT, {"ok": True, "user": "user1"})
    _add_get_slack_api_response(SLACK_CHANNEL_LIST_ENDPOINT, {"ok": True, "channels": [{"name": "slack_channel"}]})
    result = runner.invoke(
        cli.main,
        ["account", "setup"],
        input="\n".join(["   github_token   ", "y", "   slack_token   ", "   slack_channel   "]),
    )
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == "\n".join(
        [
            get_welcome_text(),
            get_github_text(),
            "GitHub token: ",
            "✓ GitHub, hello user1! 💕✨",
            "(optional) Configure Slack integration? [y/N] y",
            get_slack_text(),
            "Slack token: ",
            "Slack channel: #   slack_channel   ",
            "✓ Slack, hello user1! 🔌✨",
            "✓ Done, you can safely rerun this command at any time!\n",
        ]
    )

    settings = Settings()
    assert settings.get_github_token() == "github_token"
    assert settings.get_github_login() == "user1"
    assert settings.get_github_emails() == ["email1", "email2", "email3"]
    assert settings.get_slack_token() == "slack_token"
    assert settings.get_slack_channel() == "slack_channel"


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_ratelimit_ok(runner):
    _add_graphql_response(
        200, {"data": {"rateLimit": {"limit": 5000, "cost": 1, "remaining": 4000, "resetAt": "2019-07-11T23:39:39Z"}}}
    )
    result = runner.invoke(cli.main, ["account", "usage"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == "GitHub usage: 4000/5000 until 2019-07-11T23:39:39Z\n"
