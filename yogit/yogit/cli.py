"""
yogit entry point
"""
import click

import yogit
from yogit.yogit.logger import enable_stdout
from yogit.yogit.pullrequest import pull_request
from yogit.yogit.branch import branch
from yogit.yogit.review import review
from yogit.yogit.account import account
from yogit.yogit.scrum import scrum


@click.group()
@click.version_option(version=yogit.__version__)
@click.option("--verbose", "-v", is_flag=True, help="Print verbose output.")
@click.pass_context
def main(ctx, verbose):  # pylint: disable=unused-argument
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
