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
def test_empty_br_list_no_repo(runner):
    _add_graphql_response({"data": {"viewer": {"repositoriesContributedTo": {"edges": []}}}})
    result = runner.invoke(cli.main, ["br", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("REPO    BRANCH    PULL REQUEST\n" "------  --------  --------------\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_empty_br_list_no_branch(runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "repositoriesContributedTo": {
                        "edges": [
                            {"node": {"url": "https://", "refs": {"edges": []}}},
                            {"node": {"url": "https://", "refs": {"edges": []}}},
                        ]
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["br", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("REPO    BRANCH    PULL REQUEST\n" "------  --------  --------------\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_br_list(runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "repositoriesContributedTo": {
                        "edges": [
                            {
                                "node": {
                                    "url": "https://xyz",
                                    "refs": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "associatedPullRequests": {"edges": []},
                                                    "name": "xyz",
                                                    "target": {
                                                        "author": {"email": "user1@company1.com", "name": "user1"}
                                                    },
                                                }
                                            }
                                        ]
                                    },
                                }
                            },
                            {
                                "node": {
                                    "url": "https://xyz",
                                    "refs": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "associatedPullRequests": {"edges": []},
                                                    "name": "abc",
                                                    "target": {
                                                        "author": {"email": "user1@company3.com", "name": "user1"}
                                                    },
                                                }
                                            }
                                        ]
                                    },
                                }
                            },
                            {
                                "node": {
                                    "url": "https://abc",
                                    "refs": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "associatedPullRequests": {"edges": []},
                                                    "name": "no_pull_request",
                                                    "target": {
                                                        "author": {"email": "user1@company2.com", "name": "user1"}
                                                    },
                                                }
                                            }
                                        ]
                                    },
                                }
                            },
                            {
                                "node": {
                                    "url": "https://def",
                                    "refs": {
                                        "edges": [
                                            {
                                                "node": {
                                                    "associatedPullRequests": {
                                                        "edges": [
                                                            {"node": {"url": "https://xyz"}},
                                                            {"node": {"url": "https://abc"}},
                                                        ]
                                                    },
                                                    "name": "has_pull_request",
                                                    "target": {
                                                        "author": {"email": "user1@company3.com", "name": "user1"}
                                                    },
                                                }
                                            },
                                            {
                                                "node": {
                                                    "associatedPullRequests": {"edges": []},
                                                    "name": "notmine",
                                                    "target": {
                                                        "author": {"email": "notme@company1.fr", "name": "notme"}
                                                    },
                                                }
                                            },
                                        ]
                                    },
                                }
                            },
                        ]
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["br", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "REPO         BRANCH            PULL REQUEST\n"
        "-----------  ----------------  --------------\n"
        "https://abc  no_pull_request\n"
        "https://def  has_pull_request  https://abc\n"
        "                               https://xyz\n"
        "https://xyz  abc\n"
        "https://xyz  xyz\n"
    )
