"""
Subcommand `br`
"""

import click

from yogit.api.queries import BranchListQuery
from yogit.yogit.settings import Settings
from yogit.yogit.checks import account_required


@click.group("br")
def branch():
    """
    Branch actions
    """


@click.command("list")
@click.pass_context
@account_required
def branch_list(ctx):  # pylint: disable=unused-argument
    """
    List your branches
    """
    query = BranchListQuery(emails=Settings().get_emails())
    query.execute()
    query.print()


branch.add_command(branch_list)
