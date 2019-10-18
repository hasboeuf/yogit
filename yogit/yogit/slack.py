"""
Send report to slack
"""
import json
from yogit.yogit.settings import Settings
from yogit.api.requester import http_call


def _send_to_slack(text, thread_id=None):
    settings = Settings()
    token = settings.get_slack_token()
    channel = settings.get_slack_channel()

    webhook_url = "https://slack.com/api/chat.postMessage"

    if thread_id:
        slack_data = {
            "token": token,
            "channel": channel,
            "text": "```{}```".format(text),
            "as_user": "True",
            "thread_ts": thread_id,
        }
    else:
        slack_data = {"token": token, "channel": channel, "text": text, "as_user": "True"}

    return http_call("post", webhook_url, data=slack_data)


def send_report_to_slack(report):

    report = report.split("```")
    report_text = report[0]
    report_git = report[1]

    message = _send_to_slack(report_text)
    _send_to_slack(report_git, thread_id=message.json()["ts"])
