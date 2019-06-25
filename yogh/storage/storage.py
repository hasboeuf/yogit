"""
yogh storage
"""

import os
import json


class Storage:
    """ Storage based on JSON file """

    def __init__(self, filename):
        self.filename = filename

    def get(self, key, default=None):
        """ Get value for key """
        data = self._load_dict()
        return data.get(key, default)

    def put(self, key, value):
        """ Save value for key """
        data = self._load_dict()
        data[key] = value
        self._save_dict(data)

    def remove(self, key):
        """ Remove a key/value """
        data = self._load_dict()
        if key in data:
            del data[key]
            self._save_dict(data)

    def get_all(self):
        """ Get all key/value """
        return self._load_dict()

    def _load_dict(self):
        try:
            with open(self.filename, "r") as json_file:
                return json.load(json_file)
        except:
            return {}

    def _save_dict(self, data):
        with open(self.filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
