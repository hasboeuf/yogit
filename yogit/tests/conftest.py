from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture(scope="session", autouse=True)
def disable_spinner():
    with patch("yogit.utils.spinner.yaspin", MagicMock()):
        print("Disable spinner")
        yield


@pytest.fixture(scope="session", autouse=True)
def disable_update_check():
    with patch("yogit.yogit.checks._check_update"):
        print("Disable update check")
        yield
