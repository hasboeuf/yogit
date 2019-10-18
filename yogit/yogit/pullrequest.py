"""
Subcommand `pr`
"""

import click

from yogit.api.queries import PullRequestListQuery, OrgaPullRequestListQuery
from yogit.yogit.checks import account_required, check_update


@click.group("pr")
def pull_request():
    """
    Pull request actions
    """


@click.command("list", help="List your opened pull requests")
@click.option("--orga", type=click.STRING, help="Expand results to a specific organization")
@click.option(
    "--label",
    type=click.STRING,
    multiple=True,
    help="Only show pull requests having such label (several --label can be set)",
)
@click.pass_context
@account_required
@check_update
def pull_request_list(ctx, orga, label):  # pylint: disable=unused-argument
    """
    List pull requests
    """
    labels = [x.lower() for x in label]
    if orga:
        query = OrgaPullRequestListQuery(labels, orga)
    else:
        query = PullRequestListQuery(labels)
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


pull_request.add_command(pull_request_list)
