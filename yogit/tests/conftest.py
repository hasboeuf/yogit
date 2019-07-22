from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture(scope="session", autouse=True)
def disable_spinner():
    with patch("yogit.utils.spinner.yaspin", MagicMock()):
        print("Disable spinner")
        yield
