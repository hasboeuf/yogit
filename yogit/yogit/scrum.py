"""
Subcommand `scrum`
"""
from datetime import datetime

import click

from yogit.yogit.scrum_report import generate_scrum_report
from yogit.yogit.checks import account_required, check_update
from yogit.utils.dateutils import today_str


def _compute_date_str(str_date):
    try:
        return datetime.strptime(str_date, "%Y-%m-%d")
    except ValueError:
        raise click.ClickException("Bad date format, should be `%Y-%m-%d`")


@click.group("scrum")
def scrum():
    """
    SCRUM actions
    """


@click.command("report", help="Generate your daily activity report")
@click.option(
    "--date", "str_date", type=click.STRING, help="Date of the report", default=today_str(), show_default=True
)
@click.pass_context
@account_required
@check_update
def scrum_report(ctx, str_date):  # pylint: disable=unused-argument
    """
    Generate your daily activity report
    """
    report_dt = _compute_date_str(str_date)
    generate_scrum_report(report_dt)


scrum.add_command(scrum_report)
