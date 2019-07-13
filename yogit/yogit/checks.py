"""
yogit precheck routines
"""
import click

from yogit.yogit.settings import Settings


def account_required(func):
    """
    Check if account setup has been performed
    """

    def wrapper(self, *args, **kwargs):
        # pylint: disable=missing-docstring
        if not Settings().is_valid():
            raise click.ClickException("Account required, please `yogit account setup` first.")
        func(self, *args, **kwargs)

    return wrapper
