"""
Account commands
"""

import click

from yogit.api.queries import LoginQuery, EmailQuery, RateLimitQuery
from yogit.yogit.slack import SlackAuthCheck, SlackChannelListQuery
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

Configuration is stored here `{}`,
and is not encrypted, only use yogit on your personal computer.
""".format(
        settings.get_path()
    )


def get_github_text():
    """
    Return GitHub text
    """
    return r"""
Go here to generate a GitHub personal access token:
https://github.com/settings/tokens
Required scopes are:
• read:org
• read:user
• user:email
• repo
"""


def get_slack_text():
    """
    Return Slack text
    """
    return r"""
Go here to generate a Slack legacy token:
https://api.slack.com/custom-integrations/legacy-tokens
"""


def _setup_github():
    settings = Settings()

    if settings.is_github_valid():
        if not click.confirm("Reset GitHub config?", prompt_suffix=" "):
            return

    click.echo(get_github_text())
    token = click.prompt("GitHub token", type=click.STRING, hide_input=True).strip()
    settings.set_github_token(token)

    try:
        login_query = LoginQuery()
        login_query.execute()  # pylint: disable=no-value-for-parameter
        login = login_query.get_login()

        email_query = EmailQuery()
        email_query.execute()  # pylint: disable=no-value-for-parameter
    except Exception as exception:
        settings.reset_github()
        raise exception

    settings.set_github_login(login)
    settings.set_github_emails(email_query.get_emails())

    click.secho("✓ GitHub, hello {}! 💕✨".format(login), bold=True)


def _setup_slack():
    settings = Settings()

    if settings.is_slack_valid():
        if not click.confirm("Reset Slack config?", prompt_suffix=" "):
            return
    else:
        if not click.confirm("(optional) Configure Slack integration?", prompt_suffix=" "):
            return

    click.echo(get_slack_text())
    token = click.prompt("Slack token", type=click.STRING, hide_input=True).strip()
    channel = click.prompt("Slack channel", type=click.STRING, prompt_suffix=": #").strip()
    settings.set_slack_token(token)
    settings.set_slack_channel(channel)

    try:
        auth_query = SlackAuthCheck()
        auth_query.execute()  # pylint: disable=no-value-for-parameter
        channel_query = SlackChannelListQuery()
        channel_query.execute()
        if channel not in channel_query.channels:
            raise click.ClickException("Channel does not exist")
    except Exception as exception:
        settings.reset_slack()
        raise exception

    click.secho("✓ Slack, hello {}! 🔌✨".format(auth_query.user), bold=True)


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
    click.echo(get_welcome_text())
    _setup_github()
    _setup_slack()
    click.secho("✓ Done, you can safely rerun this command at any time!", bold=True)


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
