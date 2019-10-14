"""
Subcommand `rv`
"""

import click

from yogit.api.queries import ReviewListQuery, ReviewRequestedQuery
from yogit.yogit.checks import account_required, check_update


@click.group("review")
def review():
    """
    Review actions
    """


@click.command("list", help="List your reviews on opened pull requests")
@click.pass_context
@account_required
@check_update
def review_list(ctx):  # pylint: disable=unused-argument
    """
    List your reviews on opened pull requests
    """
    query = ReviewListQuery()
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


@click.command("requested", help="List pull requests where your review is requested")
@click.option("--missed", is_flag=True, help="Only show closed pull requests")
@click.pass_context
@account_required
@check_update
def review_requested_list(ctx, missed):  # pylint: disable=unused-argument
    """
    List pull requests where your review is requested
    """
    query = ReviewRequestedQuery(is_closed=missed)
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


review.add_command(review_list)
review.add_command(review_requested_list)
