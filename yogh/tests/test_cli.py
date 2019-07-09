import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from yogh.yogh import cli
from yogh.yogh.errors import ExitCode
from yogh.tests.mocks.mock_settings import temporary_settings


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_without_commands(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert not result.exception


@pytest.mark.usefixtures("temporary_settings")
def test_cli_account_required(runner):
    account_required_cmd_list = [
        ["account", "usage"],
        ["br", "list"],
        ["pr", "list"],
        ["rv", "requested"],
        ["scrum", "report"],
    ]

    for cmd in account_required_cmd_list:
        result = runner.invoke(cli.main, cmd)
        assert result.exit_code == ExitCode.DEFAULT_ERROR.value
        assert result.output == "Error: Account required, please `yogh account setup` first.\n"
        assert result.exception
