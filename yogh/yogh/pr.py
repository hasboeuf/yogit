"""
Subcommand `pr`
"""

import click

from yogh.yogh.logger import LOGGER, echo_info


@click.group()
def pr():
    """
    Pull request actions
    """


@click.command("list")
def pr_list():
    """
    List pull requests
    """
    echo_info("<PR LIST>")


pr.add_command(pr_list)
