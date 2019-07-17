from datetime import datetime

from unittest.mock import patch
import responses
import pytest
from click.testing import CliRunner

from yogit.yogit import cli
from yogit.yogit.errors import ExitCode
from yogit.api.client import GITHUB_API_URL_V4
from yogit.yogit.settings import ScrumReportSettings
from yogit.tests.mocks.mock_settings import mock_settings, temporary_scrum_report


def _add_graphql_response(json):
    responses.add(responses.POST, GITHUB_API_URL_V4, json=json, status=200)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.usefixtures("mock_settings")
@pytest.mark.usefixtures("temporary_scrum_report")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 7, 10, 1, 15, 59, 666))
def test_default_report_ok(utcnow_mock, runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestContributions": {
                            "edges": [
                                {"node": {"pullRequest": {"url": "https://xyz", "state": "OPEN"}}},
                                {"node": {"pullRequest": {"url": "https://abc", "state": "MERGED"}}},
                            ]
                        },
                        "pullRequestReviewContributions": {
                            "edges": [
                                {
                                    "node": {
                                        "pullRequestReview": {"url": "https://", "state": "APPROVED"},
                                        "pullRequest": {"url": "https://ghi"},
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequestReview": {"url": "https://", "state": "APPROVED"},
                                        "pullRequest": {"url": "https://def"},
                                    }
                                },
                            ]
                        },
                    }
                }
            }
        }
    )
    result = runner.invoke(
        cli.main,
        ["scrum", "report"],
        input="\n".join(["- thing1\n- thing2\n- thing3\n\n", "\n", "- thing1\n\n", "y\n", "y\n"]),
    )

    assert result.exit_code == ExitCode.NO_ERROR.value
    settings = ScrumReportSettings()
    assert result.output == "Loaded from `{}`\n".format(settings.get_path()) + (
        "What have you done today?\n"
        "Do you have any blockers?\n"
        "What do you plan to work on your next working day?\n"
        "*REPORT 2019-07-10*\n"
        "*What have you done today?*\n"
        "- thing1\n"
        "- thing2\n"
        "- thing3\n"
        "*Do you have any blockers?*\n"
        "\n"
        "*What do you plan to work on your next working day?*\n"
        "\n"
        "\n"
        "```\n"
        "PULL REQUEST    ROLE      STATE\n"
        "--------------  --------  --------\n"
        "https://abc     OWNER     MERGED\n"
        "https://def     REVIEWER  APPROVED\n"
        "https://ghi     REVIEWER  APPROVED\n"
        "https://xyz     OWNER     OPEN\n"
        "```\n"
        "Copy to clipboard? [y/N] \n"


@pytest.mark.usefixtures("mock_settings")
@pytest.mark.usefixtures("temporary_scrum_report")
@patch("yogit.yogit.settings.ScrumReportSettings.get", return_value={"invalid": "template"})
def test_report_wrong_template(mock_get_report, runner):

    result = runner.invoke(cli.main, ["scrum", "report"])
    settings = ScrumReportSettings()

    assert result.exception
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == "Loaded from `{}`\n".format(settings.get_path()) + (
        "Error: Unable to parse SCRUM report template\n"
    )


@pytest.mark.usefixtures("mock_settings")
@pytest.mark.usefixtures("temporary_scrum_report")
@patch("yogit.yogit.settings.ScrumReportSettings.get", return_value={"questions": [], "template": []})
@patch("pyperclip.copy", side_effect=Exception("error"))
def test_report_clipboard_copy_error(mock_copy, mock_get_report, runner):
    result = runner.invoke(cli.main, ["scrum", "report"], input="\n".join(["y\n"]))
    settings = ScrumReportSettings()

    assert result.exception
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == "Loaded from `{}`\n".format(settings.get_path()) + (
        "\nCopy to clipboard? [y/N] y\n" "Error: Not supported on your system, please `sudo apt-get install xclip`\n"
    )
