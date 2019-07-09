"""
Subcommand `rv`
"""

import click

from yogh.api.queries import ReviewRequestedQuery
from yogh.yogh.checks import account_required


@click.group("rv")
def review():
    """
    Review actions
    """


@click.command("requested")
@click.pass_context
@account_required
def review_requested_list(ctx):
    """
    List requested reviews
    """
    query = ReviewRequestedQuery()
    query.exec()
    query.print()


review.add_command(review_requested_list)