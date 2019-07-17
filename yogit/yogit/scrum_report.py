"""
`scrum report` command logic
"""

from string import Template

import click
import pyperclip

from yogit.yogit.logger import echo_info
from yogit.yogit.settings import ScrumReportSettings
from yogit.api.queries import PullRequestContributionListQuery
from yogit.utils.dateutils import today_str
from yogit.yogit.logger import LOGGER


def _get_github_report():
    query = PullRequestContributionListQuery()
    query.execute()
    return query.tabulate()


def generate_scrum_report():
    """
    Generate scrum report based on scrum report template

    Also copy the report in clipboard if wanted
    """
    settings = ScrumReportSettings()
    settings_data = settings.get()
    echo_info("Loaded from `{}`".format(settings.get_path()))

    data = {}
    try:
        questions = settings_data["questions"]
        tpl = settings_data["template"]
    except Exception as error:
        LOGGER.error(str(error))
        raise click.ClickException("Unable to parse SCRUM report template")

    for idx, question in enumerate(questions):
        echo_info(question)
        answers = []
        while True:
            line = input()
            if line == "":
                break
            answers.append(line)
        data["q{}".format(idx)] = question
        data["a{}".format(idx)] = "\n".join(answers)

    template = Template("\n".join(tpl))

    data["today"] = today_str()
    if "${github_report}" in template.template:
        data["github_report"] = _get_github_report()

    report = template.safe_substitute(data)
    echo_info(report)

    if click.confirm("Copy to clipboard?", prompt_suffix=" "):
        try:
            pyperclip.copy(report)
            echo_info("Copied!")
        except Exception as error:
            LOGGER.error(str(error))
            raise click.ClickException("Not supported on your system, please `sudo apt-get install xclip`")
