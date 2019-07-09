import click

from yogh.yogh.settings import Settings


def account_required(func):
    """
    Check if setup has been performed
    """

    def wrapper(self, *args, **kwargs):
        # pylint: disable=missing-docstring
        if not Settings().is_valid():
            raise click.ClickException("Account required, please `yogh account setup` first.")
        func(self, *args, **kwargs)

    return wrapper
