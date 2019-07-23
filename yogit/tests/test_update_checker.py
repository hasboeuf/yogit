from unittest.mock import patch

import responses
import pytest

from yogit.api.client import GITHUB_API_URL_V3
from yogit.yogit.update_checker import UpdateChecker, YOGIT_TAG_LIST_ENDPOINT

RESPONSE_OK = [
    {"name": "0.0.1"},
    {"name": "0.10.10"},
    {"name": "0.5.0"},
    {"name": "0.0.0"},
    {"name": "1.0.0"},
    {"name": "1.10.3"},
    {"name": "2.2.2"},
    {"name": "2.20.3"},
    {"name": "2.20.20"},
    {"name": "2.3.30"},
]


def _add_response(json):
    responses.add(responses.GET, GITHUB_API_URL_V3 + YOGIT_TAG_LIST_ENDPOINT, json=json, status=200)


@patch("yogit.yogit.update_checker.YogitTagsQuery.execute", side_effect=Exception("Error"))
def test_should_never_fail(mock_execute):
    checker = UpdateChecker()
    outdated, current_version, latest_version = checker._is_outdated()
    assert outdated == False


@patch("yogit.yogit.update_checker.get_version", return_value="2.3.30")
@responses.activate
def test_ok(mock_version):
    _add_response(RESPONSE_OK)
    checker = UpdateChecker()
    outdated, current_version, latest_version = checker._is_outdated()
    assert outdated == True
    assert current_version == "2.3.30"
    assert latest_version == "2.20.20"
