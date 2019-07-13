"""
Subcommand `scrum`
"""
import click

from yogit.yogit.scrum_report import generate_scrum_report
from yogit.yogit.checks import account_required


@click.group("scrum")
def scrum():
    """
    SCRUM actions
    """


@click.command("report")
@click.pass_context
@account_required
def scrum_report(ctx):  # pylint: disable=unused-argument
    """
    Generate your scrum report
    """
    generate_scrum_report()


scrum.add_command(scrum_report)
