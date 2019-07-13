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
def test_rv_requested_empty(runner):
    _add_graphql_response({"data": {"search": {"edges": []}}})
    result = runner.invoke(cli.main, ["rv", "requested"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("REPO    URL\n" "------  -----\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_rv_requested_ok(runner):
    _add_graphql_response(
        {
            "data": {
                "search": {
                    "edges": [
                        {"node": {"repository": {"nameWithOwner": "owner2/repo"}, "url": "https://"}},
                        {"node": {"repository": {"nameWithOwner": "owner1/repo"}, "url": "https://"}},
                    ]
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["rv", "requested"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "REPO         URL\n" "-----------  --------\n" "owner1/repo  https://\n" "owner2/repo  https://\n"
    )
