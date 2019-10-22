"""
yogit settings
"""
import yaml

from yogit.yogit.paths import get_settings_path, get_scrum_report_path
from yogit.storage.storage import Storage

SETTINGS_VERSION = 1
SCRUM_REPORT_VERSION = 2
DEFAULT_SCRUM_REPORT_CONFIG = """
# Available placeholders:
# questions: list of question to ask
# template: report template, contains one or more section.
#           each element of a section is a line, available placeholders are:
#   ${date}: "yyyy-MM-dd
#   ${qx}: x-th question
#   ${ax}: x-th answer
#   ${github_report}: GitHub activity presented in a table

questions:
- "What have you done today?"
- "Do you have any blockers?"
- "What do you plan to work on your next working day?"

template:
    sections:
    -   - "*REPORT ${date}*"
        - "*${q0}*"
        - "${a0}"
        - "*${q1}*"
        - "${a1}"
        - "*${q2}*"
        - "${a2}"
    -   - "```"
        - "${github_report}"
        - "```"
version: 2
"""


class Settings:
    """ Settings access class """

    def __init__(self):
        self.storage = Storage(get_settings_path(), SETTINGS_VERSION)

    def get_path(self):
        """
        Get storage file path
        """
        return self.storage.get_path()

    def reset(self):
        """ Reset setting values """
        self.storage.save(None)

    def is_github_valid(self):
        """ Return True if GitHub is setup, False otherwise """
        return self.get_github_token() != "" and self.get_github_login() != "" and self.get_github_emails() != []

    def reset_github(self):
        """ Reset GitHub settings """
        self.set_github_token("")
        self.set_github_login("")
        self.set_github_emails("")

    def get_github_token(self):
        """ Return GitHub token or empty string """
        data = self.storage.load()
        return data.get("token", "") or ""

    def set_github_token(self, token):
        """ Store GitHub token """
        data = self.storage.load()
        data["token"] = token
        self.storage.save(data)

    def get_github_login(self):
        """ Return GitHub login identifier or empty string """
        data = self.storage.load()
        return data.get("login", "") or ""

    def set_github_login(self, login):
        """ Store GitHub login identifier """
        data = self.storage.load()
        data["login"] = login
        self.storage.save(data)

    def get_github_emails(self):
        """ Return email list associated to the GitHub account or empty list """
        data = self.storage.load()
        return data.get("emails", []) or []

    def set_github_emails(self, emails):
        """ Store email list """
        data = self.storage.load()
        data["emails"] = emails
        self.storage.save(data)

    def is_slack_valid(self):
        """ Return True if Slack is setup, False otherwise """
        return self.get_slack_token() != "" and self.get_slack_channel() != ""

    def reset_slack(self):
        """ Reset Slack settings """
        self.set_slack_token("")
        self.set_slack_channel("")

    def set_slack_token(self, token):
        """ Store Slack token """
        data = self.storage.load()
        slack_data = data.get("slack", {}) or {}
        slack_data["legacy_token"] = token
        data["slack"] = slack_data
        self.storage.save(data)

    def get_slack_token(self):
        """ Return Slack token or empty string """
        data = self.storage.load()
        return data.get("slack", {}).get("legacy_token", "") or ""

    def set_slack_channel(self, channel):
        """ Store Slack channel """
        data = self.storage.load()
        slack_data = data.get("slack", {}) or {}
        slack_data["report_channel"] = channel
        data["slack"] = slack_data
        self.storage.save(data)

    def get_slack_channel(self):
        """ Return Slack channel or empty string """
        data = self.storage.load()
        return data.get("slack", {}).get("report_channel", "") or ""


def migrate_report_settings_from_1_to_2(data):
    """
    Migrate scrum report template of version 1 to version 2
    """
    migrated = dict()
    template_data = data.get("template", []) or []
    migrated_template = []
    for item in template_data:
        migrated_template.append(item.replace("${today}", "${date}"))
    migrated["version"] = 2
    migrated["questions"] = data.get("questions", []) or []
    migrated["template"] = {"sections": [migrated_template]}

    return migrated


class ScrumReportSettings:
    """
    Scrum report settings access class
    """

    def __init__(self):
        self.storage = Storage(get_scrum_report_path(), SCRUM_REPORT_VERSION)

    def get_path(self):
        """
        Get storage file path
        """
        return self.storage.get_path()

    def get(self):
        """
        Return scrum report data

        If not present a default one is stored and returned
        """
        data = self.storage.load()
        if data == {}:
            data = yaml.load(DEFAULT_SCRUM_REPORT_CONFIG, Loader=yaml.FullLoader)
            self.storage.save(data)
        if self.storage.get_version() is None or self.storage.get_version() == 1:
            data = migrate_report_settings_from_1_to_2(data)
            self.storage.save(data)
        return data

    def get_questions(self):
        """ Return questions or empty list """
        data = self.get()
        return data.get("questions", []) or []

    def get_template(self):
        """ Return template dict containing sections or empty dict """
        data = self.get()
        return data.get("template", {}) or {}
