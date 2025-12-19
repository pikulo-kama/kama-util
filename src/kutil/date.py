from datetime import datetime

import pytz
from babel.dates import format_datetime
from babel.localtime import get_localzone


def string_to_date(date_string: str):
    """
    Used to transform string date to actual date object.
    Uses current timezone of machine when creating date.

    Converts an ISO-formatted UTC string into a localized datetime object
    based on the system's current timezone.
    """

    creation_datetime_naive = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_datetime = pytz.utc.localize(creation_datetime_naive)
    time_zone = pytz.timezone(str(get_localzone()))

    return utc_datetime.astimezone(time_zone)


def get_verbose_date(datetime_object: datetime, locale: str, show_year: bool = True):
    """
    Used to extract date from datetime object
    and transform it to readable string.

    Formats the date according to the specified locale, with an optional
    year component.
    """

    date_format = "d MMMM"

    if show_year:
        date_format += " YYYY"

    return format_datetime(datetime_object, date_format, locale=locale)


def get_verbose_time(datetime_object: datetime, use_military: bool = False):
    """
    Used to extract time from datetime object
    and transform it to readable string.

    Formats the time into either a standard 12-hour AM/PM string or
    a 24-hour military format.
    """

    time_format = "%I:%M %p"

    if use_military:
        time_format = "%H:%M"

    return datetime_object.strftime(time_format)
