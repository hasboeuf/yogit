"""
`scrum report` command logic
"""

import re
from string import Template

import click
import pyperclip

from yogit.yogit.settings import ScrumReportSettings
from yogit.api.queries import OneDayContributionListQuery
from yogit.yogit.logger import LOGGER


def _get_github_report(report_dt):
    try:
        query = OneDayContributionListQuery(report_dt)
        query.execute()  # pylint: disable=no-value-for-parameter
        return query.tabulate()
    except Exception as exception:
        LOGGER.error(str(exception))
        return str(exception)


def generate_scrum_report(report_dt):
    """
    Generate scrum report based on scrum report template

    Also copy the report in clipboard if wanted
    """
    settings = ScrumReportSettings()
    settings_data = settings.get()
    click.secho("Tips:", bold=True)
    click.echo("• To customize report template, edit `{}`".format(settings.get_path()))
    click.echo("• Begin line with an extra " + click.style("<space>", bold=True) + " to indent it")
    click.echo("")
    click.secho("Report of {}".format(report_dt.date().isoformat()), bold=True)

    data = {}
    try:
        questions = settings_data["questions"]
        tpl = settings_data["template"]
    except Exception as error:
        LOGGER.error(str(error))
        raise click.ClickException("Unable to parse SCRUM report template")

    suffix = "• "
    for idx, question in enumerate(questions):
        click.echo(click.style(question, bold=True) + " (empty line to move on)")
        answers = []
        while True:
            line = click.prompt("", prompt_suffix=suffix, default="", show_default=False)
            if line == "":
                break
            line = suffix + line
            line = re.sub("^•  ", "    ‣ ", line)
            answers.append(line)
        data["q{}".format(idx)] = question
        data["a{}".format(idx)] = "\n".join(answers)

    template = Template("\n".join(tpl))

    data["today"] = report_dt.date().isoformat()  # "today" string does is not meaninful
    if "${github_report}" in template.template:
        data["github_report"] = _get_github_report(report_dt)

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
