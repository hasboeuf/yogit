"""
Subcommand `br`
"""

import click

from yogit.api.queries import BranchListQuery
from yogit.yogit.settings import Settings
from yogit.yogit.checks import account_required, check_update


@click.group("branch")
def branch():
    """
    Branch actions
    """


@click.command("list", help="List your branches")
@click.option("--dangling", is_flag=True, help="Only show branches which do not have associated pull requests")
@click.pass_context
@account_required
@check_update
def branch_list(ctx, dangling):  # pylint: disable=unused-argument
    """
    List your branches
    """
    query = BranchListQuery(emails=Settings().get_github_emails(), is_dangling=dangling)
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


branch.add_command(branch_list)
