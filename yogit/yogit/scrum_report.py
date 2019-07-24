"""
`scrum report` command logic
"""

from string import Template

import click
import pyperclip

from yogit.yogit.settings import ScrumReportSettings
from yogit.api.queries import PullRequestContributionListQuery
from yogit.utils.dateutils import today_str
from yogit.yogit.logger import LOGGER


def _get_github_report():
    try:
        query = PullRequestContributionListQuery()
        query.execute()  # pylint: disable=no-value-for-parameter
        return query.tabulate()
    except Exception as exception:
        LOGGER.error(str(exception))
        return str(exception)


def generate_scrum_report():
    """
    Generate scrum report based on scrum report template

    Also copy the report in clipboard if wanted
    """
    settings = ScrumReportSettings()
    settings_data = settings.get()
    click.echo("Loaded from `{}`".format(settings.get_path()))

    data = {}
    try:
        questions = settings_data["questions"]
        tpl = settings_data["template"]
    except Exception as error:
        LOGGER.error(str(error))
        raise click.ClickException("Unable to parse SCRUM report template")

    suffix = "- "
    for idx, question in enumerate(questions):
        click.echo(click.style(question, bold=True) + " (empty line to move on)")
        answers = []
        while True:
            line = click.prompt("", prompt_suffix=suffix, default="", show_default=False)
            if line == "":
                break
            answers.append(suffix + line)
        data["q{}".format(idx)] = question
        data["a{}".format(idx)] = "\n".join(answers)

    template = Template("\n".join(tpl))

    data["today"] = today_str()
    if "${github_report}" in template.template:
        data["github_report"] = _get_github_report()

    report = template.safe_substitute(data)

    if click.confirm("Copy to clipboard?", prompt_suffix=" "):
        try:
            pyperclip.copy(report)
            click.secho("Copied! 🤘", bold=True)
        except Exception as error:
            click.echo(report)
            LOGGER.error(str(error))
            raise click.ClickException("Not supported on your system, please `sudo apt-get install xclip`")
    else:
        click.echo(report)
