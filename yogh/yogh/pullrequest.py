"""
Subcommand `pr`
"""

import click

from yogh.api.queries import PullRequestListQuery
from yogh.yogh.checks import account_required


@click.group("pr")
def pull_request():
    """
    Pull request actions
    """


@click.command("list")
@click.pass_context
@account_required
def pull_request_list(ctx):
    """
    List pull requests
    """
    query = PullRequestListQuery()
    query.exec()
    query.print()


pull_request.add_command(pull_request_list)
