"""
yogit storage
"""

import os
import yaml


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
        except:
            return {}

    def save(self, data):
        with open(self.filename, "w") as yaml_file:
            if data is not None and self.version is not None:
                data["version"] = self.version
            yaml_file.write(yaml.dump(data, indent=4))

    def get_version(self):
        data = self.storage.load()
        return data.get("version", None) or None
