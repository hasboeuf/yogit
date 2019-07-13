"""
yogit settings
"""
import os
import yaml

from yogit.storage.storage import Storage

SETTINGS_DIR = os.path.join(os.path.expanduser("~/.yogit"))
SETTINGS_VERSION = 1
SCRUM_REPORT_VERSION = 1
DEFAULT_SCRUM_REPORT_CONFIG = """
# Available placeholders:
# questions: list of question to ask
# template: report template, each element is a line, available placeholders are:
#   ${today}: "yyyy-MM-dd
#   ${qx}: x-th question
#   ${ax}: x-th answer
#   ${github_report}: GitHub activity presented in a table

questions:
- "What have you done today?"
- "Do you have any blockers?"
- "What do you plan to work on on your next working day?"

template:
- "*REPORT ${today}*"
- "*${q0}*"
- "${a0}"
- "*${q1}*"
- "${a1}"
- "*${q2}*"
- "${a2}"
- ""
- "```"
- "${github_report}"
- "```"
"""


def get_log_path():
    """ Get yogit log path """
    return os.path.join(SETTINGS_DIR, "yogit.log")


def get_settings_path():
    """ Get yogit config path """
    return os.path.join(SETTINGS_DIR, "config.yaml")


def get_scrum_report_path():
    """ Get scrum report path """
    return os.path.join(SETTINGS_DIR, "scrum_report.yaml")


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

    def is_valid(self):
        """ Return True if account is setup, False otherwise """
        return self.get_token() != "" and self.get_login() != "" and self.get_emails() != []

    def get_token(self):
        """ Return GitHub token or empty string """
        data = self.storage.load()
        return data.get("token", "") or ""

    def set_token(self, token):
        """ Store GitHub token """
        data = self.storage.load()
        data["token"] = token
        self.storage.save(data)

    def get_login(self):
        """ Return login identifier or empty string """
        data = self.storage.load()
        return data.get("login", "") or ""

    def set_login(self, login):
        """ Store login identifier """
        data = self.storage.load()
        data["login"] = login
        self.storage.save(data)

    def get_emails(self):
        """ Return email list associated to the GitHub account or empty list """
        data = self.storage.load()
        return data.get("emails", []) or []

    def set_emails(self, emails):
        """ Store email list """
        data = self.storage.load()
        data["emails"] = emails
        self.storage.save(data)


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
        return data
