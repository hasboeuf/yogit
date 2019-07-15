"""
Subcommand `pr`
"""

import click

from yogit.api.queries import PullRequestListQuery
from yogit.yogit.checks import account_required


@click.group("pr")
def pull_request():
    """
    Pull request actions
    """


@click.command("list")
@click.pass_context
@account_required
def pull_request_list(ctx):  # pylint: disable=unused-argument
    """
    List pull requests
    """
    query = PullRequestListQuery()
    query.execute()
    query.print()


pull_request.add_command(pull_request_list)
