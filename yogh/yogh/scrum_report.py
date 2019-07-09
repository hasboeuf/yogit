from string import Template

import click
import pyperclip

from yogh.yogh.logger import echo_info
from yogh.storage.storage import Storage
from yogh.yogh.settings import ScrumReportSettings
from yogh.api.queries import PullRequestContributionListQuery
from yogh.utils.dateutils import today_str


def _get_github_report():
    query = PullRequestContributionListQuery()
    query.exec()
    return query.tabulate()


class ScrumReport:
    def exec(self):
        settings = ScrumReportSettings()
        settings_data = settings.load()
        echo_info("Loaded from `{}`".format(settings.path))

        data = {}
        for idx, question in enumerate(settings_data["questions"]):
            echo_info(question)
            answers = []
            while True:
                line = input()
                if line == "":
                    break
                answers.append(line)
            data["q{}".format(idx)] = question
            data["a{}".format(idx)] = "\n".join(answers)

        template = Template("\n".join(settings_data["template"]))

        data["today"] = today_str()
        if "${github_report}" in template.template:
            data["github_report"] = _get_github_report()

        report = template.safe_substitute(data)
        echo_info(report)

        if click.confirm("Copy to clipboard?", prompt_suffix=" "):
            try:
                pyperclip.copy(report)
                echo_info("Copied!")
            except pyperclip.PyperclipException:
                echo_info("Not supported on your system, please `sudo apt-get install xclip`")
