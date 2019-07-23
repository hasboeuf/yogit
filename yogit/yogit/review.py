"""
Subcommand `rv`
"""

import click

from yogit.api.queries import ReviewListQuery, ReviewRequestedQuery
from yogit.yogit.checks import account_required


@click.group("rv")
def review():
    """
    Review actions
    """


@click.command("list", help="List your reviews on opened pull requests")
@click.pass_context
@account_required
def review_list(ctx):  # pylint: disable=unused-argument
    """
    List your reviews on opened pull requests
    """
    query = ReviewListQuery()
    query.execute()
    query.print()


@click.command("requested", help="List pull requests where your review is requested")
@click.pass_context
@account_required
def review_requested_list(ctx):  # pylint: disable=unused-argument
    """
    List pull requests where your review is requested
    """
    query = ReviewRequestedQuery()
    query.execute()
    query.print()


review.add_command(review_list)
review.add_command(review_requested_list)
