"""
GraphQL requesters used by yogh
"""
from yogh.yogh.settings import Settings
import yogh.api.statements as S
from yogh.utils.dateutils import today_earliest_str


def prepare(statement, tokens):
    """
    Set tokens in statement and return the prepared statement
    """
    prepared_statement = statement
    for token in tokens:
        if token == S.LOGIN_TOKEN:
            prepared_statement = prepared_statement.replace(token, Settings().get_login())
        elif token == S.TODAY_TOKEN:
            prepared_statement = prepared_statement.replace(token, today_earliest_str())
    return prepared_statement
