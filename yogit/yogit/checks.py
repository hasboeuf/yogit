"""
yogit precheck routines
"""
import click

from yogit.yogit.settings import Settings
from yogit.yogit.update_checker import UpdateChecker


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


def _check_update():
    UpdateChecker().check()


def check_update(func):
    """
    Check if a new version of yogit is available
    """

    def wrapper(self, *args, **kwargs):
        # pylint: disable=missing-docstring
        _check_update()
        func(self, *args, **kwargs)

    return wrapper
