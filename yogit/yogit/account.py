"""
Account commands
"""

import click

from yogit.api.queries import LoginQuery, EmailQuery, RateLimitQuery
from yogit.yogit.settings import Settings
from yogit.yogit.checks import account_required, check_update


def get_welcome_text():
    """
    Return Welcome text
    """
    settings = Settings()
    return r"""                   _ _
 _   _  ___   __ _(_) |_ 
| | | |/ _ \ / _` | | __|
| |_| | (_) | (_| | | |_ 
 \__, |\___/ \__, |_|\__|
 |___/       |___/       

Welcome to yogit!

Go here to generate a GitHub personal access token:
https://github.com/settings/tokens
Required scopes are:
• read:org
• read:user
• user:email
• repo

Configuration is stored here `{}`,
and is not encrypted, only use yogit on your personal computer.
""".format(
        settings.get_path()
    )


@click.group("account")
def account():
    """
    Account actions
    """


@click.command("setup", help="Setup yogit")
def account_setup():
    """
    Setup yogit
    """
    settings = Settings()
    settings.reset()

    click.echo(get_welcome_text())
    token = click.prompt("GitHub token", type=click.STRING, hide_input=True).strip()

    settings.set_token(token)

    try:
        login_query = LoginQuery()
        login_query.execute()  # pylint: disable=no-value-for-parameter
        login = login_query.get_login()

        email_query = EmailQuery()
        email_query.execute()  # pylint: disable=no-value-for-parameter
    except Exception as exception:
        settings.reset()
        raise exception

    settings.set_login(login)
    settings.set_emails(email_query.get_emails())

    click.secho("Hello {}! 💕✨".format(login), bold=True)


@click.command("usage", help="Account API usage")
@click.pass_context
@account_required
@check_update
def account_usage(ctx):  # pylint: disable=unused-argument
    """
    Account API usage
    """
    query = RateLimitQuery()
    query.execute()  # pylint: disable=no-value-for-parameter
    query.print()


account.add_command(account_setup)
account.add_command(account_usage)
