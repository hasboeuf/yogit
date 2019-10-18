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
    assert result.output == ("Nothing... 😿 Time to push hard 💪\n")


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
                            {
                                "node": {
                                    "createdAt": "2019-05-27T18:00:01Z",
                                    "url": "https://xyz",
                                    "title": "title9",
                                    "mergeable": "UNKNOWN",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-05-28T08:00:01Z",
                                    "url": "https://abc",
                                    "title": "title8",
                                    "mergeable": "MERGEABLE",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-07-02T19:00:59Z",
                                    "url": "https://xyz",
                                    "title": "title7",
                                    "mergeable": "CONFLICTED",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-07-02T18:00:30Z",
                                    "url": "https://abc",
                                    "title": "title6",
                                    "mergeable": "MERGEABLE",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-07-11T19:00:30Z",
                                    "url": "https://xyz",
                                    "title": "title5",
                                    "mergeable": "CONFLICTED",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-07-11T19:00:30Z",
                                    "url": "https://efg",
                                    "title": "title4",
                                    "mergeable": "MERGEABLE",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-07-11T17:00:30Z",
                                    "url": "https://abc",
                                    "title": "title3",
                                    "mergeable": "CONFLICTED",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-07-12T13:00:01Z",
                                    "url": "https://xyz",
                                    "title": "title2",
                                    "mergeable": "MERGEABLE",
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-07-12T13:00:01Z",
                                    "url": "https://abc",
                                    "title": "title1",
                                    "mergeable": "CONFLICTED",
                                }
                            },
                        ]
                    }
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["pr", "list"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "CREATED      URL          TITLE    MERGEABLE\n"
        "-----------  -----------  -------  -----------\n"
        "Today        https://abc  title1   CONFLICTED\n"
        "Today        https://xyz  title2   MERGEABLE\n"
        "Yesterday    https://abc  title3   CONFLICTED\n"
        "Yesterday    https://efg  title4   MERGEABLE\n"
        "Yesterday    https://xyz  title5   CONFLICTED\n"
        "10 days ago  https://abc  title6   MERGEABLE\n"
        "10 days ago  https://xyz  title7   CONFLICTED\n"
        "45 days ago  https://abc  title8   MERGEABLE\n"
        "46 days ago  https://xyz  title9   UNKNOWN\n"
        "Count: 9\n"
    )


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 10, 18, 1, 15, 59, 666))
def test_pr_list_with_label_filter_ok(mock_utc_now, runner):
    _add_graphql_response(
        {
            "data": {
                "viewer": {
                    "pullRequests": {
                        "edges": [
                            {
                                "node": {
                                    "createdAt": "2019-10-17T18:00:01Z",
                                    "url": "https://xyz",
                                    "title": "title1",
                                    "mergeable": "MERGEABLE",
                                    "labels": {"edges": [{"node": {"name": "LaBeL1"}}, {"node": {"name": "lAbEl2"}}]},
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-10-16T08:00:01Z",
                                    "url": "https://abc",
                                    "title": "title2",
                                    "mergeable": "MERGEABLE",
                                    "labels": {"edges": [{"node": {"name": "LaBeL1"}}, {"node": {"name": "lAbEl3"}}]},
                                }
                            },
                            {
                                "node": {
                                    "createdAt": "2019-10-15T19:00:59Z",
                                    "url": "https://xyz",
                                    "title": "title3",
                                    "mergeable": "MERGEABLE",
                                    "labels": {"edges": []},
                                }
                            },
                        ]
                    }
                }
            }
        }
    )

    result = runner.invoke(cli.main, ["pr", "list", "--label", "label1"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "CREATED     URL          TITLE    MERGEABLE\n"
        "----------  -----------  -------  -----------\n"
        "Yesterday   https://xyz  title1   MERGEABLE\n"
        "2 days ago  https://abc  title2   MERGEABLE\n"
        "Count: 2\n"
    )

    result = runner.invoke(cli.main, ["pr", "list", "--label", "LABEL1", "--label", "label3"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "CREATED     URL          TITLE    MERGEABLE\n"
        "----------  -----------  -------  -----------\n"
        "2 days ago  https://abc  title2   MERGEABLE\n"
        "Count: 1\n"
    )


@pytest.mark.usefixtures("mock_settings")
@responses.activate
def test_pr_list_with_unknown_orga(runner):
    _add_graphql_response({"data": {"search": {"pageInfo": {"hasNextPage": False, "endCursor": None}, "edges": []}}})
    result = runner.invoke(cli.main, ["pr", "list", "--orga", "unknown"])
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == ("Nothing... 😿 Time to push hard 💪\n")


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 7, 17, 8, 15, 30, 666))
def test_pr_list_with_orga_ok(mock_utc_now, runner):
    _add_graphql_response(
        {
            "data": {
                "search": {
                    "pageInfo": {"hasNextPage": True, "endCursor": "cursor_id"},
                    "edges": [
                        {"node": {"createdAt": "2019-07-17T10:30:15Z", "url": "https://xyz", "title": "title2"}},
                        {"node": {"createdAt": "2019-07-17T17:28:15Z", "url": "https://abc", "title": "title1"}},
                    ],
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
                        {"node": {"createdAt": "2019-06-17T01:18:00Z", "url": "https://xyz", "title": "title3"}},
                        {"node": {"createdAt": "2019-05-17T08:36:15Z", "url": "https://abc", "title": "title4"}},
                    ],
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["pr", "list", "--orga", "Orga"])
    print(str(result.exception))
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "CREATED      URL          TITLE\n"
        "-----------  -----------  -------\n"
        "Today        https://abc  title1\n"
        "Today        https://xyz  title2\n"
        "30 days ago  https://xyz  title3\n"
        "61 days ago  https://abc  title4\n"
        "Count: 4\n"
    )


@pytest.mark.usefixtures("mock_settings")
@responses.activate
@patch("yogit.utils.dateutils._utcnow", return_value=datetime(2019, 10, 18, 8, 15, 30, 666))
def test_pr_list_with_orga_with_label_filter_ok(mock_utc_now, runner):
    _add_graphql_response(
        {
            "data": {
                "search": {
                    "pageInfo": {"hasNextPage": True, "endCursor": "cursor_id"},
                    "edges": [
                        {
                            "node": {
                                "createdAt": "2019-07-17T10:30:15Z",
                                "url": "https://xyz",
                                "title": "title1",
                                "labels": {
                                    "edges": [{"node": {"name": "LaBeL with spacE"}}, {"node": {"name": "lAbEl2"}}]
                                },
                            }
                        },
                        {
                            "node": {
                                "createdAt": "2019-07-17T17:28:15Z",
                                "url": "https://abc",
                                "title": "title2",
                                "labels": {"edges": []},
                            }
                        },
                    ],
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
                        {
                            "node": {
                                "createdAt": "2019-06-17T01:18:00Z",
                                "url": "https://xyz",
                                "title": "title3",
                                "labels": {"edges": []},
                            }
                        },
                        {
                            "node": {
                                "createdAt": "2019-05-17T08:36:15Z",
                                "url": "https://abc",
                                "title": "title4",
                                "labels": {
                                    "edges": [{"node": {"name": "LaBeL with spacE"}}, {"node": {"name": "lAbEl3"}}]
                                },
                            }
                        },
                    ],
                }
            }
        }
    )
    result = runner.invoke(cli.main, ["pr", "list", "--orga", "Orga", "--label", "label with SpAce"])
    print(str(result.exception))
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "CREATED       URL          TITLE\n"
        "------------  -----------  -------\n"
        "93 days ago   https://xyz  title1\n"
        "154 days ago  https://abc  title4\n"
        "Count: 2\n"
    )

    result = runner.invoke(
        cli.main, ["pr", "list", "--orga", "Orga", "--label", "label with SpAce", "--label", "label3"]
    )
    print(str(result.exception))
    assert result.exit_code == ExitCode.NO_ERROR.value
    assert result.output == (
        "CREATED       URL          TITLE\n"
        "------------  -----------  -------\n"
        "154 days ago  https://abc  title4\n"
        "Count: 1\n"
    )
