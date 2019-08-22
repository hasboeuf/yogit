"""
Subcommand `orga`
"""
import random
from time import sleep

import click

from yogit.api.queries import OrganizationMemberListQuery
from yogit.yogit.checks import account_required, check_update
from yogit.utils.spinner import get_spinner_object


@click.group("orga")
def organization():
    """
    Organization actions
    """


@click.group("member")
def member():
    """
    Member actions
    """


@click.command("list", help="List members of the organization you belong to")
@click.pass_context
@account_required
@check_update
def orga_member_list(ctx):  # pylint: disable=unused-argument
    """
    List members of the organization you belong to
    """
    query = OrganizationMemberListQuery()
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


@click.command("pickone", help="Randomly pick a member of the organization you belong to")
@click.pass_context
@account_required
@check_update
def orga_member_pickone(ctx):  # pylint: disable=unused-argument
    """
    Randomly pick a member of the organization you belong to
    """
    query = OrganizationMemberListQuery()
    query.execute()  # pylint: disable=no-value-for-parameter
    members = [x[0] for x in query.data]
    count = len(members)
    click.secho("Picking out one out of {} members... ({:.2f}%) 🎲".format(count, 100 / count), bold=True)
    random.seed()
    with get_spinner_object() as spinner:
        for _ in range(20):  # Rolling for 5 seconds
            picked_member = members[random.randint(0, count - 1)]
            spinner.text = picked_member
            sleep(0.25)
    click.secho('The winner is "{}" 🤠'.format(picked_member), bold=True)


organization.add_command(member)
member.add_command(orga_member_list)
member.add_command(orga_member_pickone)
