from datetime import datetime

from unittest.mock import patch, MagicMock
import responses
import pytest
from click.testing import CliRunner

from yogit.yogit import cli
from yogit.yogit.errors import ExitCode
from yogit.api.client import GITHUB_API_URL_V4
from yogit.yogit.slack import SLACK_API_URL, SLACK_POST_MESSAGE_ENDPOINT, SLACK_MESSAGE_LINK_ENDPOINT
from yogit.yogit.settings import Settings, ScrumReportSettings
from yogit.tests.mocks.mock_settings import mock_settings, temporary_scrum_report


def _add_graphql_response(json):
    responses.add(responses.POST, GITHUB_API_URL_V4, json=json, status=200)


def _add_post_slack_api_response(endpoint, json):
    responses.add(responses.POST, SLACK_API_URL + endpoint, json=json, status=200)


def _add_get_slack_api_response(endpoint, json):
    responses.add(responses.GET, SLACK_API_URL + endpoint, json=json, status=200)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.usefixtures("mock_settings")
def test_wrong_date(runner):
    result = runner.invoke(cli.main, ["scrum", "report", "--date", "badformat"])
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == ("Error: Bad date format, should be `%Y-%m-%d`\n")


@pytest.mark.usefixtures("mock_settings")
@pytest.mark.usefixtures("temporary_scrum_report")
@patch("yogit.yogit.settings.ScrumReportSettings.get", return_value={"questions": [], "template": {"sections": []}})
@responses.activate
def test_with_specific_date(mock_get_report, runner):
    Settings().reset_slack()
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestContributions": {"edges": []},
                        "pullRequestReviewContributions": {"edges": []},
                    }
                }
            }
        }
    )

    result = runner.invoke(cli.main, ["scrum", "report", "--date", "2019-06-05"], input="\n".join(["n\n"]))

    assert result.exit_code == ExitCode.NO_ERROR.value
    report_settings = ScrumReportSettings()
    assert result.output == (
        "Tips:\n"
        "• To customize report template, edit `{}`\n"
        "• Begin line with an extra <space> to indent it\n"
        "\n"
        "Today's cheat sheet 😏:\n"
        "• Sorry, nothing from GitHub may be you can ask your mum? 🤷‍\n"
        "\n"
        "Report of 2019-06-05\n"
        "Copy to clipboard? [y/N] n\n"
        "\n"
    ).format(report_settings.get_path())


@pytest.mark.usefixtures("mock_settings")
@pytest.mark.usefixtures("temporary_scrum_report")
@responses.activate
@patch("yogit.yogit.scrum._compute_date_str", return_value=datetime(2019, 7, 10, 1, 15, 59, 666))
@patch("pyperclip.copy")
def test_default_report_ok(mock_copy, mock_compute_date, runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestContributions": {
                            "edges": [
                                {
                                    "node": {
                                        "pullRequest": {"url": "https://xyz", "state": "OPEN", "title": "Title xyz"}
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequest": {"url": "https://abc", "state": "MERGED", "title": "Title abc"}
                                    }
                                },
                            ]
                        },
                        "pullRequestReviewContributions": {
                            "edges": [
                                {
                                    "node": {
                                        "pullRequestReview": {"url": "https://", "state": "APPROVED"},
                                        "pullRequest": {"url": "https://ghi", "title": "Title ghi"},
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequestReview": {"url": "https://", "state": "APPROVED"},
                                        "pullRequest": {"url": "https://def", "title": "Title def"},
                                    }
                                },
                            ]
                        },
                    }
                }
            }
        }
    )

    _add_post_slack_api_response(SLACK_POST_MESSAGE_ENDPOINT, {"ok": True, "ts": "1"})
    _add_get_slack_api_response(SLACK_MESSAGE_LINK_ENDPOINT, {"ok": True, "permalink": "https://link"})

    # Test with slack post and report copy
    result = runner.invoke(
        cli.main, ["scrum", "report"], input="\n".join(["thing1\nthing2\nthing3\n", "", "thing1\n", "y", "y"])
    )
    assert result.exit_code == ExitCode.NO_ERROR.value
    settings = ScrumReportSettings()
    assert result.output == (
        "Tips:\n"
        "• To customize report template, edit `{}`\n"
        "• Begin line with an extra <space> to indent it\n"
        "\n"
        "Today's cheat sheet 😏:\n"
        "• Title abc (owner)\n"
        "• Title def (reviewer)\n"
        "• Title ghi (reviewer)\n"
        "• Title xyz (owner)\n"
        "\n"
        "Report of 2019-07-10\n"
        "What have you done today? (empty line to move on)\n"
        "• thing1\n"
        "• thing2\n"
        "• thing3\n"
        "• \n"
        "Do you have any blockers? (empty line to move on)\n"
        "• \n"
        "What do you plan to work on your next working day? (empty line to move on)\n"
        "• thing1\n"
        "• \n"
        "Send to Slack? [y/N] y\n"
        "Sent! 🤘 https://link\n"
        "Copy to clipboard? [y/N] y\n"
        "Copied! 🤘\n"
    ).format(settings.get_path())

    # Test without slack post, without report copy and with extra indentation
    result = runner.invoke(
        cli.main,
        ["scrum", "report"],
        input="\n".join(
            ["thing1:", " subthing1", " subthing2", " subthing3", "thing2", "thing3\n", "", "thing1\n", "n", "n"]
        ),
    )

    assert result.exit_code == ExitCode.NO_ERROR.value
    settings = ScrumReportSettings()
    assert result.output == (
        "Tips:\n"
        "• To customize report template, edit `{}`\n"
        "• Begin line with an extra <space> to indent it\n"
        "\n"
        "Today's cheat sheet 😏:\n"
        "• Title abc (owner)\n"
        "• Title def (reviewer)\n"
        "• Title ghi (reviewer)\n"
        "• Title xyz (owner)\n"
        "\n"
        "Report of 2019-07-10\n"
        "What have you done today? (empty line to move on)\n"
        "• thing1:\n"
        "•  subthing1\n"
        "•  subthing2\n"
        "•  subthing3\n"
        "• thing2\n"
        "• thing3\n"
        "• \n"
        "Do you have any blockers? (empty line to move on)\n"
        "• \n"
        "What do you plan to work on your next working day? (empty line to move on)\n"
        "• thing1\n"
        "• \n"
        "Send to Slack? [y/N] n\n"
        "Copy to clipboard? [y/N] n\n"
        "*REPORT 2019-07-10*\n"
        "*What have you done today?*\n"
        "• thing1:\n"
        "    ‣ subthing1\n"
        "    ‣ subthing2\n"
        "    ‣ subthing3\n"
        "• thing2\n"
        "• thing3\n"
        "*Do you have any blockers?*\n"
        "\n"
        "*What do you plan to work on your next working day?*\n"
        "• thing1\n"
        "```\n"
        "PULL REQUEST    ROLE      STATE\n"
        "--------------  --------  --------\n"
        "https://abc     OWNER     MERGED\n"
        "https://def     REVIEWER  APPROVED\n"
        "https://ghi     REVIEWER  APPROVED\n"
        "https://xyz     OWNER     OPEN\n"
        "```\n"
    ).format(settings.get_path())


@pytest.mark.usefixtures("mock_settings")
@pytest.mark.usefixtures("temporary_scrum_report")
@patch("yogit.yogit.settings.ScrumReportSettings.get", return_value={"questions": [], "template": {"sections": []}})
@patch("yogit.yogit.scrum_report._exec_github_report_query", return_value=MagicMock())
@patch("pyperclip.copy", side_effect=Exception("error"))
@patch("yogit.yogit.scrum._compute_date_str", return_value=datetime(2019, 8, 20, 1, 15, 59, 666))
def test_report_clipboard_copy_error(mock_compute_date, mock_copy, mock_query, mock_get_report, runner):
    Settings().reset_slack()
    result = runner.invoke(cli.main, ["scrum", "report"], input="\n".join(["y\n"]))
    report_settings = ScrumReportSettings()

    assert result.exception
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == (
        "Tips:\n"
        "• To customize report template, edit `{}`\n"
        "• Begin line with an extra <space> to indent it\n"
        "\n"
        "Today's cheat sheet 😏:\n"
        "• Sorry, nothing from GitHub may be you can ask your mum? 🤷‍\n"
        "\n"
        "Report of 2019-08-20\n"
        "Copy to clipboard? [y/N] y\n"
        "\n"
        "Error: Not supported on your system, please `sudo apt-get install xclip`\n"
    ).format(report_settings.get_path())
