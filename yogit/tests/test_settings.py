import pytest


from yogit.tests.mocks.mock_settings import temporary_settings, assert_empty_settings
from yogit.yogit.settings import Settings


@pytest.mark.usefixtures("temporary_settings")
def test_empty_settings():
    settings = Settings()
    assert settings.get_token() == ""
    assert settings.get_login() == ""
    assert settings.get_emails() == []


@pytest.mark.usefixtures("temporary_settings")
def test_set_get_reset_settings():
    settings = Settings()
    settings.set_token("token")
    settings.set_login("login")
    settings.set_emails(["email1", "email2", "email3"])

    assert settings.get_token() == "token"
    assert settings.get_login() == "login"
    assert settings.get_emails() == ["email1", "email2", "email3"]

    settings.reset()

    assert_empty_settings()
