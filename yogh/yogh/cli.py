"""
yogh entry point
"""
import click

import yogh
from yogh.yogh.logger import enable_stdout
from yogh.yogh.pr import pr


@click.group()
@click.version_option(version=yogh.__version__)
@click.option("--verbose", "-v", is_flag=True, help="Print verbose output.")
@click.pass_context
def main(ctx, verbose):
    """
    Command line utility for GitHub daily work
    """
    if verbose:
        enable_stdout()


main.add_command(pr)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
