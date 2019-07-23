"""
Application logger
"""

import logging
import os
import sys

from yogit import get_name, get_version
from yogit.yogit.paths import get_log_path, SETTINGS_DIR


def get_logger(stdout=False, logger_name=get_name(), version=get_version()):
    """
    Create and configure a logger using a given name.
    """
    os.makedirs(SETTINGS_DIR, exist_ok=True)

    application_str = logger_name
    if version:
        application_str += " " + version
    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s "
            "[{application}:%(process)d] "
            "[%(levelname)s] "
            "%(message)s".format(application=application_str)
        ),
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    file_log_handler = logging.FileHandler(get_log_path())
    file_log_handler.setLevel(logging.DEBUG)
    file_log_handler.setFormatter(formatter)

    local_logger = logging.getLogger(logger_name)
    local_logger.setLevel(logging.DEBUG)
    local_logger.addHandler(file_log_handler)

    if stdout:
        console_log_handler = logging.StreamHandler(sys.stdout)
        console_log_handler.setLevel(logging.DEBUG)
        console_log_handler.setFormatter(formatter)
        local_logger.addHandler(console_log_handler)

    return local_logger


LOGGER = get_logger()


def enable_stdout():
    """
    Prints logs in stdout
    """
    global LOGGER  # pylint: disable=global-statement
    LOGGER = get_logger(stdout=True)
