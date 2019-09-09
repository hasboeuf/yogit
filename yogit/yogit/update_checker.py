"""
Check for yogit update
"""
from functools import cmp_to_key
from packaging import version

import click

from yogit import get_version
from yogit.api.queries import RESTQuery
from yogit.yogit.logger import LOGGER

YOGIT_TAG_LIST_ENDPOINT = "/repos/hasboeuf/yogit/tags"


def compare(version1, version2):
    """
    Compare two X.Y.Z version string, can be used in sorted() function
    """
    if version1 == version2:
        return 0
    return -1 if version.parse(version1) < version.parse(version2) else 1


class YogitTagsQuery(RESTQuery):
    """
    Fetch tags from yogit repository
    """

    def __init__(self):
        super().__init__("/repos/hasboeuf/yogit/tags")
        self.tags = []

    def _handle_response(self, response):
        self.tags = [x["name"] for x in response]

    def get_tags(self):
        """
        Return fetched tags
        """
        return self.tags


class UpdateChecker:
    """
    Check is yogit is updatable
    """

    def __init__(self):
        self.query = YogitTagsQuery()

    def _is_outdated(self):
        current_version = get_version()
        try:
            self.query.execute()
            tags = sorted(self.query.get_tags(), key=cmp_to_key(compare), reverse=True)
            latest_version = tags[0]
            outdated = version.parse(current_version) < version.parse(latest_version)
        except Exception as exception:
            # Update check should never fail
            LOGGER.error(str(exception))
            return False, current_version, current_version
        return outdated, current_version, latest_version

    def check(self):
        """
        Compare current version with the latest one and print a message if needed
        """
        outdated, current_version, latest_version = self._is_outdated()
        if not outdated:
            return
        click.secho(
            (
                "You are using yogit {current_version}, however version {latest_version} is available 🎁\n"
                "You can upgrade it with `pip3 install --upgrade yogit` 🚀\n"
                "Changelog: https://github.com/hasboeuf/yogit/blob/{latest_version}/CHANGELOG.md"
            ).format(current_version=current_version, latest_version=latest_version),
            fg="yellow",
        )
