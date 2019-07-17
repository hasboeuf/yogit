"""
Subcommand `pr`
"""

import click

from yogit.api.queries import PullRequestListQuery, OrgaPullRequestListQuery
from yogit.yogit.checks import account_required


@click.group("pr")
def pull_request():
    """
    Pull request actions
    """


@click.command("list")
@click.option("--orga", type=click.STRING, help="List all opened pull requests of an organization")
@click.pass_context
@account_required
def pull_request_list(ctx, orga):  # pylint: disable=unused-argument
    """
    List pull requests
    """
    if orga:
        query = OrgaPullRequestListQuery(orga)
    else:
        query = PullRequestListQuery()
    query.execute()
    query.print()


pull_request.add_command(pull_request_list)
