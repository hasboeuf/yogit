"""
Account commands
"""

import click

from yogit.yogit.logger import echo_info
from yogit.api.queries import LoginQuery, EmailQuery, RateLimitQuery
from yogit.yogit.settings import Settings
from yogit.yogit.checks import account_required


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
- admin:org
- repo
- user

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


@click.command("setup")
def account_setup():
    """
    Setup yogit
    """
    settings = Settings()
    settings.reset()

    echo_info(get_welcome_text())
    token = click.prompt("GitHub token", type=click.STRING, hide_input=True)

    query = LoginQuery(token)
    query.exec()
    login = query.get_login()

    settings.set_token(token)
    settings.set_login(login)

    query = EmailQuery()
    query.exec()
    settings.set_emails(query.get_emails())

    echo_info("Hello {}!".format(login))


@click.command("usage")
@click.pass_context
@account_required
def account_usage(ctx):  # pylint: disable=unused-argument
    """
    Current API usage
    """
    query = RateLimitQuery()
    query.exec()
    query.print()


account.add_command(account_setup)
account.add_command(account_usage)
