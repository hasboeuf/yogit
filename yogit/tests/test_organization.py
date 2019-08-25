from unittest.mock import patch, Mock, MagicMock
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
def test_orga_member_list_no_oranization(runner):
    _add_graphql_response({"data": {"viewer": {"organizations": {"edges": []}}}})
    result = runner.invoke(cli.main, ["orga", "member", "list"])
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == ("Error: You do not belong to any organization 😿\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_orga_member_list_more_than_one_oranization(runner):
    _add_graphql_response({"data": {"viewer": {"organizations": {"edges": [{}, {}]}}}})
    result = runner.invoke(cli.main, ["orga", "member", "list"])
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == ("Error: You belong to more than one organization, this is not yet supported 😿\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_orga_member_list_ok(runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "organizations": {
                        "edges": [
                            {
                                "node": {
                                    "name": "Company",
                                    "membersWithRole": {
                                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                                        "edges": [
                                            {
                                                "role": "MEMBER",
                                                "node": {
                                                    "login": "user3",
                                                    "email": "user3@company.com",
                                                    "location": "San Francisco",
                                                },
                                            },
                                            {
                                                "role": "ADMIN",
                                                "node": {
                                                    "login": "user2",
                                                    "email": "user2@company.com",
                                                    "location": "Lyon",
                                                },
                                            },
                                            {
                                                "role": "ADMIN",
                                                "node": {
                                                    "login": "user1",
                                                    "email": "user1@company.com",
                                                    "location": "Besancon",
                                                },
                                            },
                                        ],
                                    },
                                }
                            }
                        ]
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["orga", "member", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "Company's members\n"
        "NAME    EMAIL              LOCATION       ROLE\n"
        "------  -----------------  -------------  ------\n"
        "user1   user1@company.com  Besancon       ADMIN\n"
        "user2   user2@company.com  Lyon           ADMIN\n"
        "user3   user3@company.com  San Francisco  MEMBER\n"
        "Count: 3\n"
    )


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.yogit.organization.OrganizationMemberListQuery", return_value=MagicMock())
@patch("yogit.yogit.organization.sleep", return_value=0)
@patch("yogit.yogit.organization.random.randint", return_value=2)
def test_orga_member_pickone(mock_random, mock_sleep, mock_query, runner):
    mock_query.return_value.data = [["user1"], ["user2"], ["user3"]]
    result = runner.invoke(cli.main, ["orga", "member", "pickone"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("Picking one out of 3 members... (33.33%) 🎲\n" 'The winner is "user3" 🤠\n')
