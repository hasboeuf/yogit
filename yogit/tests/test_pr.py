from datetime import datetime

from unittest.mock import patch
import responses
import pytest
from click.testing import CliRunner

from yogit.yogit import cli
from yogit.yogit.errors import ExitCode
from yogit.api.client import GITHUB_API_URL_V4
from yogit.tests.mocks.mock_settings import mock_settings


def _add_graphql_response(json):
    responses.add(responses.POST, GITHUB_API_URL_V4, json=json, status=200)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_empty_pr_list(runner):
    _add_graphql_response({"data": {"viewer": {"pullRequests": {"edges": []}}}})
    result = runner.invoke(cli.main, ["pr", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("CREATED    URL    TITLE\n" "---------  -----  -------\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 7, 12, 1, 15, 59, 666))
def test_pr_list_ok(mock_utc_now, runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "pullRequests": {
                        "edges": [
                            {"node": {"createdAt": "2019-05-28T18:00:01Z", "url": "https://xyz", "title": "title1"}},
                            {"node": {"createdAt": "2019-05-28T08:00:01Z", "url": "https://abc", "title": "title2"}},
                            {"node": {"createdAt": "2019-07-02T18:00:59Z", "url": "https://xyz", "title": "title3"}},
                        ]
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["pr", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "CREATED      URL          TITLE\n"
        "-----------  -----------  -------\n"
        "9 days ago   https://xyz  title3\n"
        "44 days ago  https://abc  title2\n"
        "44 days ago  https://xyz  title1\n"
    )
