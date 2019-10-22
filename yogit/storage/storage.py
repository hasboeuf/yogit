"""
yogit storage
"""

import os
import yaml

import click

from yogit.yogit.logger import LOGGER


class Storage:
    """ Storage based on YAML file """

    def __init__(self, filename, version=None):
        self.filename = filename
        self.version = version

    def get_path(self):
        """
        Get storage file path
        """
        return self.filename

    def load(self):
        """ Load YAML """
        try:
            with open(self.filename, "r") as yaml_file:
                return yaml.load(yaml_file, Loader=yaml.FullLoader) or {}
        except OSError as error:
            LOGGER.error(str(error))
            return {}
        except Exception as error:
            raise click.ClickException("Cannot parse `{}`: {}".format(self.get_path(), str(error)))
            LOGGER.error(str(error))

    def save(self, data):
        with open(self.filename, "w") as yaml_file:
            if data is not None and self.version is not None:
                data["version"] = self.version
            yaml.safe_dump(data, stream=yaml_file, indent=4)

    def get_version(self):
        data = self.load()
        return data.get("version", None) or None
