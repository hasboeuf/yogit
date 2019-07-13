import tempfile
from unittest.mock import patch
import pytest

from yogit.yogit.settings import Settings


@pytest.fixture(scope="function")
def temporary_scrum_report():
    """
    Make scrum report use temporary config file
    """

    with tempfile.NamedTemporaryFile() as scrum_report_file:
        print("Using scrum report `%s`" % scrum_report_file.name)
        with patch("yogit.yogit.settings.get_scrum_report_path", return_value=scrum_report_file.name):
            yield


@pytest.fixture(scope="function")
def temporary_settings():
    """
    Make settings use temporary config file
    """

    with tempfile.NamedTemporaryFile() as settings_file:
        print("Using temporary settings `%s`" % settings_file.name)
        with patch("yogit.yogit.settings.get_settings_path", return_value=settings_file.name):
            yield


@pytest.fixture(scope="function")
def mock_settings():
    """
    Make settings use temporary config file and fill them
    """

    with tempfile.NamedTemporaryFile() as settings_file:
        print("Using mock settings `%s`" % settings_file.name)
        with patch("yogit.yogit.settings.get_settings_path", return_value=settings_file.name):
            fill_settings()
            yield


def fill_settings():
    settings = Settings()
    settings.set_emails(["user1@company1.com", "user1@company2.com", "user1@company3.com"])
    settings.set_login("user1")
    settings.set_token("<token>")


def assert_empty_settings():
    settings = Settings()
    assert settings.get_token() == ""
    assert settings.get_login() == ""
    assert settings.get_emails() == []
