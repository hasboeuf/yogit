"""
`scrum report` command logic
"""

import re
from string import Template

import click
import pyperclip

from yogit.yogit.settings import ScrumReportSettings, Settings
from yogit.api.queries import OneDayContributionListQuery
from yogit.yogit.logger import LOGGER
from yogit.yogit.slack import SlackPostMessageQuery


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
    report_settings = ScrumReportSettings()
    report_data = report_settings.get()
    click.secho("Tips:", bold=True)
    click.echo("• To customize report template, edit `{}`".format(report_settings.get_path()))
    click.echo("• Begin line with an extra " + click.style("<space>", bold=True) + " to indent it")
    click.echo("")
    click.secho("Report of {}".format(report_dt.date().isoformat()), bold=True)

    data = {}
    try:
        questions = report_data["questions"]
        tpl = report_data["template"]
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

    settings = Settings()
    if settings.is_slack_valid():
        if click.confirm("Send to Slack?", prompt_suffix=" "):
            try:
                query = SlackPostMessageQuery(report)
                query.execute()
                click.secho("Sent! 🤘", bold=True)
                # TODO print message link
            except Exception as error:
                click.secho("Failed to send", bold=True)
                LOGGER.error(str(error))

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
