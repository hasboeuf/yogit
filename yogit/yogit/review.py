"""
Subcommand `rv`
"""

import click

from yogit.api.queries import ReviewRequestedQuery
from yogit.yogit.checks import account_required


@click.group("rv")
def review():
    """
    Review actions
    """


@click.command("requested")
@click.pass_context
@account_required
def review_requested_list(ctx):  # pylint: disable=unused-argument
    """
    List requested reviews
    """
    query = ReviewRequestedQuery()
    query.execute()
    query.print()


review.add_command(review_requested_list)
