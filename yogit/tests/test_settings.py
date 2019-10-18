import pytest


from yogit.tests.mocks.mock_settings import temporary_settings, assert_empty_settings
from yogit.yogit.settings import Settings


@pytest.mark.usefixtures("temporary_settings")
def test_empty_settings():
    settings = Settings()
    assert not settings.is_github_valid()
    assert not settings.is_slack_valid()
    assert_empty_settings()


@pytest.mark.usefixtures("temporary_settings")
def test_set_get_reset_settings():
    settings = Settings()
    settings.set_github_token("github_token")
    settings.set_github_login("github_login")
    settings.set_github_emails(["github_email1", "github_email2", "github_email3"])

    assert settings.is_github_valid()
    assert not settings.is_slack_valid()
    assert settings.get_github_token() == "github_token"
    assert settings.get_github_login() == "github_login"
    assert settings.get_github_emails() == ["github_email1", "github_email2", "github_email3"]

    settings.set_slack_token("slack_token")
    settings.set_slack_channel("slack_channel")

    assert settings.is_github_valid()
    assert settings.is_slack_valid()
    assert settings.get_slack_token() == "slack_token"
    assert settings.get_slack_channel() == "slack_channel"

    settings.reset_slack()
    assert not settings.is_slack_valid()
    settings.reset_github()
    assert not settings.is_github_valid()
    assert_empty_settings()
