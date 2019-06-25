"""
yogh settings
"""
import os

SETTINGS_DIR = os.path.join(os.path.expanduser("~/.yogh"))


def get_log_path():
    """ Get yogh log path """
    return os.path.join(SETTINGS_DIR, "yogh.log")
