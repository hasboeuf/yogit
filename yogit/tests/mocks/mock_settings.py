import os
import tempfile
from contextlib import contextmanager
from unittest.mock import patch

import pytest

from yogit.yogit.settings import Settings


@contextmanager
def named_temporary_file(*args, **kwds):
    """
    Context manager to handle temp file on all OS.

    Windows does not allow processes other than the one used to create the NamedTemporaryFile
    to access the file when using delete=True (the default).
    => Closing the file manually.
    """
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    try:
        yield tmpfile
    finally:
        tmpfile.close()
        os.unlink(tmpfile.name)


@pytest.fixture(scope="function")
def temporary_scrum_report():
    """
    Make scrum report use temporary config file
    """

    with named_temporary_file() as scrum_report_file:
        print("Using scrum report `%s`" % scrum_report_file.name)
        with patch("yogit.yogit.settings.get_scrum_report_path", return_value=scrum_report_file.name):
            yield


@pytest.fixture(scope="function")
def temporary_settings():
    """
    Make settings use temporary config file
    """

    with named_temporary_file() as settings_file:
        print("Using temporary settings `%s`" % settings_file.name)
        with patch("yogit.yogit.settings.get_settings_path", return_value=settings_file.name):
            yield


@pytest.fixture(scope="function")
def mock_settings():
    """
    Make settings use temporary config file and fill them
    """

    with named_temporary_file() as settings_file:
        print("Using mock settings `%s`" % settings_file.name)
        with patch("yogit.yogit.settings.get_settings_path", return_value=settings_file.name):
            fill_settings()
            yield


def fill_settings():
    settings = Settings()
    settings.set_github_emails(["user1@company1.com", "user1@company2.com", "user1@company3.com"])
    settings.set_github_login("user1")
    settings.set_github_token("github_token")
    settings.set_slack_token("slack_token")
    settings.set_slack_channel("slack_channel")


def assert_empty_settings():
    settings = Settings()
    assert settings.get_github_token() == ""
    assert settings.get_github_login() == ""
    assert settings.get_github_emails() == []
    assert settings.get_slack_token() == ""
    assert settings.get_slack_channel() == ""
