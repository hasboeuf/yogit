import pytest


from yogit.tests.mocks.mock_settings import temporary_settings, assert_empty_settings, temporary_scrum_report
from yogit.yogit.settings import Settings, ScrumReportSettings

REPORT_TEMPLATE_1 = r"""
questions:
- "What have you done today?"
- "Do you have any blockers?"
- "What do you plan to work on your next working day?"
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

REPORT_TEMPLATE_2 = r"""questions:
- What have you done today?
- Do you have any blockers?
- What do you plan to work on your next working day?
template:
    sections:
    -   - '*REPORT ${date}*'
        - '*${q0}*'
        - ${a0}
        - '*${q1}*'
        - ${a1}
        - '*${q2}*'
        - ${a2}
    -   - '```'
        - ${github_report}
        - '```'
version: 2
"""


@pytest.mark.usefixtures("temporary_settings")
def test_empty_settings():
    settings = Settings()
    assert not settings.is_github_valid()
    assert not settings.is_slack_valid()
    assert_empty_settings()


@pytest.mark.usefixtures("temporary_settings")
def test_set_get_reset_settings():
    settings = Settings()
    settings.set_github_token("github_token")
    settings.set_github_login("github_login")
    settings.set_github_emails(["github_email1", "github_email2", "github_email3"])

    assert settings.is_github_valid()
    assert not settings.is_slack_valid()
    assert settings.get_github_token() == "github_token"
    assert settings.get_github_login() == "github_login"
    assert settings.get_github_emails() == ["github_email1", "github_email2", "github_email3"]

    settings.set_slack_token("slack_token")
    settings.set_slack_channel("slack_channel")

    assert settings.is_github_valid()
    assert settings.is_slack_valid()
    assert settings.get_slack_token() == "slack_token"
    assert settings.get_slack_channel() == "slack_channel"

    settings.reset_slack()
    assert not settings.is_slack_valid()
    settings.reset_github()
    assert not settings.is_github_valid()
    assert_empty_settings()


@pytest.mark.usefixtures("temporary_scrum_report")
def test_report_settings_1_to_2_migration():
    report_settings = ScrumReportSettings()

    with open(report_settings.storage.get_path(), "w") as settings_file:
        settings_file.write(REPORT_TEMPLATE_1)

    report_settings.get()

    with open(report_settings.storage.get_path(), "r") as settings_file:
        content = settings_file.read()
        assert content == REPORT_TEMPLATE_2
