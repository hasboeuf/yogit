""" Date utility functions """
from datetime import datetime


def _utcnow():
    return datetime.utcnow()


def dt_for_str(dt_string):
    """ Return datetime object from ISO 8601 string """
    return datetime.strptime(dt_string, r"%Y-%m-%dT%H:%M:%SZ")


def utcnow_str():
    """ Return ISO 8601 string of now instant """
    return _utcnow().replace(microsecond=0).isoformat()


def today_str():
    """ Return ISO 8601 string of today """
    return _utcnow().strftime(r"%Y-%m-%d")


def today_earliest_str():
    """ Return ISO 8601 string of the begining of today """
    return _utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()


def days_ago_str(dte):
    """ Return human readable string between today and another date object """
    today = _utcnow().date()
    delta_days = (today - dte).days
    if delta_days == 0:
        return "Today"
    if delta_days == 1:
        return "Yesterday"
    return "{} days ago".format(delta_days)
