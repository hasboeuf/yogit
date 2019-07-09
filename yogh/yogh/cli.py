"""
yogh entry point
"""
import click

import yogh
from yogh.yogh.logger import enable_stdout
from yogh.yogh.pullrequest import pull_request
from yogh.yogh.branch import branch
from yogh.yogh.review import review
from yogh.yogh.account import account
from yogh.yogh.scrum import scrum


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


main.add_command(account)
main.add_command(branch)
main.add_command(pull_request)
main.add_command(review)
main.add_command(scrum)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
