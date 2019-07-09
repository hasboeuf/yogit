"""
Subcommand `br`
"""

import click

from yogh.api.queries import BranchListQuery
from yogh.yogh.settings import Settings
from yogh.yogh.checks import account_required


@click.group("br")
def branch():
    """
    Branch actions
    """


@click.command("list")
@click.pass_context
@account_required
def branch_list(ctx):
    """
    List your branches
    """
    query = BranchListQuery(emails=Settings().get_emails())
    query.exec()
    query.print()


branch.add_command(branch_list)
