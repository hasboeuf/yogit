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
from yogit.yogit.slack import SlackPostMessageQuery, SlackMessageLinkQuery


def _exec_github_report_query(report_dt):
    try:
        query = OneDayContributionListQuery(report_dt)
        query.execute()  # pylint: disable=no-value-for-parameter
        return query
    except Exception as exception:
        LOGGER.exception(str(exception))
        raise exception


def generate_scrum_report(report_dt):
    """
    Generate scrum report based on scrum report template

    Also copy the report in clipboard if wanted
    """
    report_settings = ScrumReportSettings()
    click.secho("Tips:", bold=True)
    click.echo("• To customize report template, edit `{}`".format(report_settings.get_path()))
    click.echo("• Begin line with an extra " + click.style("<space>", bold=True) + " to indent it")
    click.echo("")

    report_query = _exec_github_report_query(report_dt)
    click.secho("Today's cheat sheet 😏:", bold=True)
    if len(report_query.data) == 0:
        click.echo("• Sorry, nothing from GitHub may be you can ask your mum? 🤷‍")
    else:
        for contrib in report_query.get_contrib_str():
            click.echo("• {}".format(contrib))
    click.echo("")

    data = {}
    questions = report_settings.get_questions()
    tpl = report_settings.get_template()
    suffix = "• "

    click.secho("Report of {}".format(report_dt.date().isoformat()), bold=True)
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

    report_sections = []
    for section in tpl.get("sections", []):
        template = Template("\n".join(section))
        data["date"] = report_dt.date().isoformat()
        if "${github_report}" in template.template:
            data["github_report"] = report_query.tabulate()
        report_sections.append(template.safe_substitute(data))

    settings = Settings()
    if settings.is_slack_valid():
        if click.confirm("Send to Slack?", prompt_suffix=" "):
            try:
                first_query = None
                for section in report_sections:
                    query = SlackPostMessageQuery(section, reply_to=first_query)
                    query.execute()
                    if first_query is None:
                        first_query = query
                query = SlackMessageLinkQuery(first_query)
                query.execute()
                click.secho("Sent! 🤘 {}".format(query.url), bold=True)
            except Exception as error:
                click.secho("Failed to send: {}".format(str(error)), bold=True)
                LOGGER.error(str(error))

    report = "\n".join(report_sections)
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
