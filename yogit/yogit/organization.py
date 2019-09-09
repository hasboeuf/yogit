"""
Subcommand `orga`
"""
import random
from time import sleep

import click

from yogit.api.queries import OrganizationListQuery, OrganizationMemberListQuery
from yogit.yogit.checks import account_required, check_update
from yogit.utils.spinner import get_spinner_object


def check_organization(orga):
    """
    Check if orga exist or if user belong to only one orga
    """
    query = OrganizationListQuery()
    query.execute()
    orgas = [x[0].lower() for x in query.data]
    if not orgas:
        raise click.ClickException("You do not belong to any organization 😿")
    if orga is None:
        if len(orgas) == 1:
            return orgas[0]
        raise click.ClickException(
            "You belong to more than one organization (see `yogit orga list`), use `--orga` option to discriminate"
        )
    if orga.lower() not in orgas:
        raise click.ClickException("Unrecognized {} organization (see `yogit orga list`)".format(orga))
    return orga


@click.group("orga")
def organization():
    """
    Organization actions
    """


@click.command("list", help="List organizations you belong to")
@click.pass_context
@account_required
@check_update
def orga_list(ctx):  # pylint: disable=unused-argument
    """
    List organizations you belong to
    """
    query = OrganizationListQuery()
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


@click.group("member")
def member():
    """
    Member actions
    """


@click.command("list", help="List members of the organization you belong to")
@click.option("--orga", type=click.STRING, help="Specify the organization")
@click.pass_context
@account_required
@check_update
def orga_member_list(ctx, orga):  # pylint: disable=unused-argument
    """
    List members of the organization you belong to
    """
    orga = check_organization(orga)
    query = OrganizationMemberListQuery(orga)
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


@click.command("pickone", help="Randomly pick a member of the organization you belong to")
@click.option("--orga", type=click.STRING, help="Specify the organization")
@click.pass_context
@account_required
@check_update
def orga_member_pickone(ctx, orga):  # pylint: disable=unused-argument
    """
    Randomly pick a member of the organization you belong to
    """
    orga = check_organization(orga)
    query = OrganizationMemberListQuery(orga)
    query.execute()  # pylint: disable=no-value-for-parameter
    members = [x[0] for x in query.data]
    count = len(members)
    click.secho("Picking one out of {} members... ({:.2f}%) 🎲".format(count, 100 / count), bold=True)
    random.seed()
    with get_spinner_object() as spinner:
        for _ in range(20):  # Rolling for 5 seconds
            picked_member = members[random.randint(0, count - 1)]
            spinner.text = picked_member
            sleep(0.25)
    click.secho('The winner is "{}" 🤠'.format(picked_member), bold=True)


organization.add_command(orga_list)
organization.add_command(member)
member.add_command(orga_member_list)
member.add_command(orga_member_pickone)
