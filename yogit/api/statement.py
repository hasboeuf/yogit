"""
GraphQL requesters used by yogit
"""
from string import Template

from yogit.yogit.settings import Settings
import yogit.api.statements as S
from yogit.utils.dateutils import today_earliest_str


def prepare(statement, variables):
    """
    Set variable in statement and return the prepared statement
    """
    template = Template(statement)
    data = {}
    for variable in variables:
        if variable == S.LOGIN_VARIABLE:
            data[variable] = Settings().get_login()
        elif variable == S.TODAY_VARIABLE:
            data[variable] = today_earliest_str()
    return template.safe_substitute(data)


def prepare_pagination(statement, offset, cursor=None):
    template = Template(statement)
    data = {"offset": offset, "after": 'after: "{}"'.format(cursor) if cursor is not None else ""}
    return template.safe_substitute(data)
