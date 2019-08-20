from datetime import datetime

from unittest.mock import patch
import responses
import pytest
from click.testing import CliRunner

from yogit.yogit import cli
from yogit.yogit.errors import ExitCode
from yogit.api.client import GITHUB_API_URL_V4
from yogit.tests.mocks.mock_settings import mock_settings
from yogit.utils.dateutils import today_str


def _add_graphql_response(json):
    responses.add(responses.POST, GITHUB_API_URL_V4, json=json, status=200)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_empty_ct_list(runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestContributions": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "edges": []}
                    }
                }
            }
        }
    )
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
    result = runner.invoke(cli.main, ["ct", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("Contributions from {} to {}\n" "Nothing... 😿 Time to push hard 💪\n").format(
        today_str(), today_str()
    )


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch(
    "yogit.yogit.contribution._compute_date_str",
    return_value=(datetime(2019, 7, 10, 1, 15, 59, 666), datetime(2019, 7, 10, 1, 15, 59, 666)),
)
def test_ct_list_today_ok(mock_compute_date, runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestContributions": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "edges": [
                                {
                                    "node": {
                                        "pullRequest": {
                                            "url": "https://def",
                                            "title": "Title 2",
                                            "createdAt": "2019-08-19T14:46:19Z",
                                        }
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequest": {
                                            "url": "https://abc",
                                            "title": "Title 1",
                                            "createdAt": "2019-08-19T14:40:17Z",
                                        }
                                    }
                                },
                            ],
                        }
                    }
                }
            }
        }
    )
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestReviewContributions": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "edges": [
                                {
                                    "node": {
                                        "pullRequestReview": {"publishedAt": "2019-08-19T11:56:25Z"},
                                        "pullRequest": {"url": "https://xyz", "title": "Title 4"},
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequestReview": {"publishedAt": "2019-08-19T11:56:25Z"},
                                        "pullRequest": {"url": "https://ghi", "title": "Title 3"},
                                    }
                                },
                            ],
                        }
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["ct", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "Contributions from {} to {}\n"
        "CREATED     PULL REQUEST    ROLE      TITLE\n"
        "----------  --------------  --------  -------\n"
        "2019-08-19  https://abc     OWNER     Title 1\n"
        "2019-08-19  https://def     OWNER     Title 2\n"
        "2019-08-19  https://ghi     REVIEWER  Title 3\n"
        "2019-08-19  https://xyz     REVIEWER  Title 4\n"
        "Count: 4\n"
    ).format(today_str(), today_str())


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_ct_list_ok(runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestContributions": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "edges": [
                                {
                                    "node": {
                                        "pullRequest": {
                                            "url": "https://def",
                                            "title": "Title 2",
                                            "createdAt": "2019-08-19T14:46:19Z",
                                        }
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequest": {
                                            "url": "https://def",
                                            "title": "Title 5",
                                            "createdAt": "2019-08-01T14:46:19Z",
                                        }
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequest": {
                                            "url": "https://abc",
                                            "title": "Title 1",
                                            "createdAt": "2019-08-19T14:40:17Z",
                                        }
                                    }
                                },
                            ],
                        }
                    }
                }
            }
        }
    )
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "pullRequestReviewContributions": {
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                            "edges": [
                                {
                                    "node": {
                                        "pullRequestReview": {"publishedAt": "2019-08-15T11:56:25Z"},
                                        "pullRequest": {"url": "https://xyz", "title": "Title 3"},
                                    }
                                },
                                {
                                    "node": {
                                        "pullRequestReview": {"publishedAt": "2019-08-11T11:56:25Z"},
                                        "pullRequest": {"url": "https://ghi", "title": "Title 4"},
                                    }
                                },
                            ],
                        }
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["ct", "list", "--from", "2019-08-01", "--to", "2019-08-15"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "Contributions from 2019-08-01 to 2019-08-15\n"
        "CREATED     PULL REQUEST    ROLE      TITLE\n"
        "----------  --------------  --------  -------\n"
        "2019-08-19  https://abc     OWNER     Title 1\n"
        "2019-08-19  https://def     OWNER     Title 2\n"
        "2019-08-15  https://xyz     REVIEWER  Title 3\n"
        "2019-08-11  https://ghi     REVIEWER  Title 4\n"
        "2019-08-01  https://def     OWNER     Title 5\n"
        "Count: 5\n"
    )


@pytest.mark.usefixtures("mock_settings")
def test_wrong_dates(runner):
    for args in [
        ["ct", "list", "--from", "badformat"],
        ["ct", "list", "--to", "badformat"],
        ["ct", "list", "--from", "badformat", "--to", "badformat"],
    ]:
        result = runner.invoke(cli.main, args)
        assert result.exit_code == ExitCode.DEFAULT_ERROR.value
        assert result.output == ("Error: Bad date format, should be `%Y-%m-%d`\n")


@pytest.mark.usefixtures("mock_settings")
def test_range_too_large(runner):
    result = runner.invoke(cli.main, ["ct", "list", "--from", "2019-08-01", "--to", "2020-08-02"])
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == ("Error: Date range must not exceed one year\n")


@pytest.mark.usefixtures("mock_settings")
def test_to_earlier_than_from(runner):
    result = runner.invoke(cli.main, ["ct", "list", "--from", "2019-08-02", "--to", "2019-08-01"])
    assert result.exit_code == ExitCode.DEFAULT_ERROR.value
    assert result.output == ("Error: `--from` is not before `--to`\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_empty_ct_stats_ok(runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "contributionsCollection": {
                        "totalIssueContributions": 0,
                        "totalCommitContributions": 1,
                        "totalRepositoryContributions": 2,
                        "totalPullRequestContributions": 30,
                        "totalPullRequestReviewContributions": 31,
                        "totalRepositoriesWithContributedIssues": 400,
                        "totalRepositoriesWithContributedCommits": 401,
                        "totalRepositoriesWithContributedPullRequests": 5000,
                        "totalRepositoriesWithContributedPullRequestReviews": 5001,
                    }
                }
            }
        }
    )

    result = runner.invoke(cli.main, ["ct", "stats"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "STAT                                                        VALUE\n"
        "--------------------------------------------------------  -------\n"
        "Total commit contributions                                      1\n"
        "Total issue contributions                                       0\n"
        "Total pull request contributions                               30\n"
        "Total pull request review contributions                        31\n"
        "Total repositories with contributed commits                   401\n"
        "Total repositories with contributed issues                    400\n"
        "Total repositories with contributed pull request reviews     5001\n"
        "Total repositories with contributed pull requests            5000\n"
        "Total repository contributions                                  2\n"
    )
