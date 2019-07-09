"""
Subcommand `scrum`
"""
import click

from yogh.yogh.scrum_report import ScrumReport
from yogh.yogh.checks import account_required


@click.group("scrum")
def scrum():
    """
    SCRUM actions
    """


@click.command("report")
@click.pass_context
@account_required
def scrum_report(ctx):
    """
    Generate your scrum report
    """
    report = ScrumReport()
    report.exec()


scrum.add_command(scrum_report)
