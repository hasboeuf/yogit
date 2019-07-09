from unittest.mock import patch
import pytest

from yogh.api.statement import prepare
import yogh.api.statements as S
from yogh.tests.mocks.mock_settings import mock_settings


@pytest.mark.usefixtures("mock_settings")
def test_prepare_no_token():
    statement = """
    {
        login: @login@,
        date: @today@
    }
    """
    assert prepare(statement, []) == statement


@pytest.mark.usefixtures("mock_settings")
def test_prepare_only_one_token():
    statement = """
    {
        login: @login@,
        date: @today@
    }
    """
    assert (
        prepare(statement, [S.LOGIN_TOKEN])
        == """
    {
        login: user1,
        date: @today@
    }
    """
    )


@pytest.mark.usefixtures("mock_settings")
@patch("yogh.api.statement.today_earliest_str", return_value="2019-07-01")
def test_prepare_all_tokens(mock_today_earliest_str):
    statement = """
    {
        login: @login@,
        date: @today@
    }
    """
    assert (
        prepare(statement, [S.LOGIN_TOKEN, S.TODAY_TOKEN])
        == """
    {
        login: user1,
        date: 2019-07-01
    }
    """
    )
