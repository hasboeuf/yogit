"""
yogh entry point
"""
import click

import yogh
from yogh.yogh.logger import LOGGER
from yogh.yogh.pr import pr


@click.group()
@click.version_option(version=yogh.__version__)
@click.pass_context
def main(ctx):
    """
    Command line utility for GitHub daily work
    """


main.add_command(pr)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
