"""
Subcommand `ct`
"""
from datetime import datetime

import click

from yogit.api.queries import ContributionListQuery, ContributionStatsQuery
from yogit.yogit.checks import account_required, check_update
from yogit.utils.dateutils import today_str


def _compute_date_str(str_from, str_to):
    try:
        dt_from = datetime.strptime(str_from, "%Y-%m-%d")
        dt_to = datetime.strptime(str_to, "%Y-%m-%d")
        dt_to = dt_to.replace(hour=23, minute=59, second=59, microsecond=0)
    except ValueError:
        raise click.ClickException("Bad date format, should be `%Y-%m-%d`")
    if dt_from > dt_to:
        raise click.ClickException("`--from` is not before `--to`")
    return dt_from, dt_to


def _get_default_to():
    return today_str()


def _get_default_from():
    return today_str()


@click.group("contrib")
def contribution():
    """
    Contribution actions
    """


@click.command("list", help="List your contributions")
@click.option(
    "--to",
    "str_to",
    type=click.STRING,
    help="End search at this date (included)",
    default=_get_default_to(),
    show_default=True,
)
@click.option(
    "--from",
    "str_from",
    type=click.STRING,
    help="Begin search at this date",
    default=_get_default_from(),
    show_default=True,
)
@click.pass_context
@account_required
@check_update
def contribution_list(ctx, str_from, str_to):  # pylint: disable=unused-argument
    """
    List contributions
    """
    dt_from, dt_to = _compute_date_str(str_from, str_to)
    if (dt_to - dt_from).days > 365:
        raise click.ClickException("Date range must not exceed one year")
    click.secho("Contributions from {} to {}".format(str_from, str_to), bold=True)
    query = ContributionListQuery(dt_from, dt_to)
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


@click.command("stats", help="GitHub statistics")
@click.pass_context
@account_required
@check_update
def contribution_stats(ctx):  # pylint: disable=unused-argument
    """
    List GitHub statistics
    """
    query = ContributionStatsQuery()
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


contribution.add_command(contribution_list)
contribution.add_command(contribution_stats)
