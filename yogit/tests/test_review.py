from unittest.mock import patch
from datetime import datetime

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
def test_rv_list_empty(runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestReviewContributions": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "edges": [],
                        }
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["review", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("Nothing... 😿\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 7, 17, 1, 15, 59, 666))
def test_rv_list_ok(mock_utc_now, runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestReviewContributions": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "edges": [
                                {"node": {"pullRequest": {"state": "MERGED"}}},
                                {
                                    "node": {
                                        "pullRequestReview": {
                                            "createdAt": "2019-07-16T14:44:46Z",
                                            "updatedAt": None,
                                            "state": "APPROVED",
                                        },
                                        "pullRequest": {
                                            "url": "https://abc",
                                            "state": "OPEN",
                                            "commits": {
                                                "edges": [{"node": {"commit": {"pushedDate": "2019-07-16T14:27:26Z"}}}]
                                            },
                                        },
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequestReview": {
                                            "createdAt": "2019-07-15T10:44:46Z",
                                            "updatedAt": "2019-07-16T20:44:46Z",
                                            "state": "COMMENTED",
                                        },
                                        "pullRequest": {
                                            "url": "https://xyz",
                                            "state": "OPEN",
                                            "commits": {
                                                "edges": [{"node": {"commit": {"pushedDate": "2019-07-16T14:27:26Z"}}}]
                                            },
                                        },
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequestReview": {
                                            "createdAt": "2019-06-01T10:26:46Z",
                                            "updatedAt": "2019-07-10T14:44:46Z",
                                            "state": "APPROVED",
                                        },
                                        "pullRequest": {
                                            "url": "https://abc",
                                            "state": "OPEN",
                                            "commits": {
                                                "edges": [{"node": {"commit": {"pushedDate": "2019-07-16T14:27:26Z"}}}]
                                            },
                                        },
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequestReview": {
                                            "createdAt": "2019-03-10T18:30:00Z",
                                            "updatedAt": None,
                                            "state": "APPROVED",
                                        },
                                        "pullRequest": {
                                            "url": "https://def",
                                            "state": "OPEN",
                                            "commits": {
                                                "edges": [{"node": {"commit": {"pushedDate": "2019-07-16T14:27:26Z"}}}]
                                            },
                                        },
                                    }
                                },
                            ],
                        }
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["review", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "UPDATED       PULL REQUEST    STATE\n"
        "------------  --------------  ----------------------\n"
        "Yesterday     https://abc     APPROVED\n"
        "Yesterday     https://xyz     COMMENTED\n"
        "7 days ago    https://abc     APPROVED (new commits)\n"
        "129 days ago  https://def     APPROVED (new commits)\n"
        "Count: 4\n"
    )


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_rv_requested_empty(runner):
    _add_graphql_response({"data": {"search": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "edges": []}}})
    result = runner.invoke(cli.main, ["review", "requested"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("All done! 🎉✨\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 10, 14, 1, 15, 59, 666))
def test_rv_requested_ok(mock_utc_now, runner):
    _add_graphql_response(
        {
            "data": {
                "search": {
                    "pageInfo": {"hasNextPage": True, "endCursor": "cursor_id"},
                    "edges": [{"node": {"url": "https://def", "title": "def", "updatedAt": "2019-10-14T20:44:46Z"}}],
                }
            }
        }
    )
    _add_graphql_response(
        {
            "data": {
                "search": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "edges": [
                        {"node": {"url": "https://repo/pull/1", "title": "abc", "updatedAt": "2019-10-10T10:44:46Z"}},
                        {"node": {"url": "https://repo/pull/2", "title": "xyz", "updatedAt": "2019-10-10T20:44:46Z"}},
                    ],
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["review", "requested"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "UPDATED     PULL REQUEST         TITLE\n"
        "----------  -------------------  -------\n"
        "Today       https://def          def\n"
        "4 days ago  https://repo/pull/1  abc\n"
        "4 days ago  https://repo/pull/2  xyz\n"
        "Count: 3\n"
    )


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 10, 14, 1, 15, 59, 666))
def test_rv_requested_missed_ok(mock_utc_now, runner):
    _add_graphql_response(
        {
            "data": {
                "search": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "edges": [
                        {"node": {"url": "https://repo/pull/1", "title": "abc", "updatedAt": "2019-10-10T10:44:46Z"}},
                        {"node": {"url": "https://repo/pull/2", "title": "xyz", "updatedAt": "2019-10-10T20:44:46Z"}},
                    ],
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["review", "requested", "--missed"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "UPDATED     PULL REQUEST         TITLE\n"
        "----------  -------------------  -------\n"
        "4 days ago  https://repo/pull/1  abc\n"
        "4 days ago  https://repo/pull/2  xyz\n"
        "Count: 2\n"
    )
