"""
Subcommand `scrum`
"""
import click

from yogit.yogit.scrum_report import generate_scrum_report
from yogit.yogit.checks import account_required, check_update


@click.group("scrum")
def scrum():
    """
    SCRUM actions
    """


@click.command("report", help="Generate your daily activity report")
@click.pass_context
@account_required
@check_update
def scrum_report(ctx):  # pylint: disable=unused-argument
    """
    Generate your daily activity report
    """
    generate_scrum_report()


scrum.add_command(scrum_report)
