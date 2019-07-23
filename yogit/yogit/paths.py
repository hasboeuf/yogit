"""
yogit paths
"""
import os

SETTINGS_DIR = os.path.join(os.path.expanduser("~/.yogit"))


def get_log_path():
    """ Get yogit log path """
    return os.path.join(SETTINGS_DIR, "yogit.log")


def get_settings_path():
    """ Get yogit config path """
    return os.path.join(SETTINGS_DIR, "config.yaml")


def get_scrum_report_path():
    """ Get scrum report path """
    return os.path.join(SETTINGS_DIR, "scrum_report.yaml")
