"""
Subcommand `br`
"""

import click

from yogit.api.queries import BranchListQuery
from yogit.yogit.settings import Settings
from yogit.yogit.checks import account_required, check_update


@click.group("br")
def branch():
    """
    Branch actions
    """


@click.command("list", help="List your branches")
@click.pass_context
@account_required
@check_update
def branch_list(ctx):  # pylint: disable=unused-argument
    """
    List your branches
    """
    query = BranchListQuery(emails=Settings().get_emails())
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


branch.add_command(branch_list)
