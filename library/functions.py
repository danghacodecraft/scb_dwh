import json
import re
from datetime import date, datetime

from config.settings import DATETIME_INPUT_OUTPUT_FORMAT


def decode_to_json(data):
    return json.loads(data)


def today():
    return date.today()


def now():
    return datetime.now()


def datetime_to_string(_time: datetime, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> str:
    if _time:
        return _time.strftime(_format)
    return ''


def string_to_datetime(string: str, default=None, _format=DATETIME_INPUT_OUTPUT_FORMAT) -> datetime:
    try:
        return datetime.strptime(string, _format)
    except (ValueError, TypeError):
        return default


def string_to_int(string: str, default=None) -> int:
    try:
        return int(string)
    except (ValueError, TypeError):
        return default


def date_to_datetime(date_input: date, default=None) -> datetime:
    try:
        return datetime.combine(date_input, datetime.min.time())
    except (ValueError, TypeError):
        return default


def datetime_to_date(datetime_input: datetime, default=None) -> date:
    try:
        return datetime_input.date()
    except (ValueError, TypeError):
        return default


def end_time_of_day(datetime_input: datetime, default=None) -> datetime:
    try:
        return datetime_input.replace(hour=23, minute=59, second=59)
    except (ValueError, TypeError):
        return default


def is_valid_url(url):
    pattern = r"^(https|http)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$"
    if re.match(pattern, url):
        return True
    else:
        return False


def concat_url_and_parameters(parameter: dict, url: str) -> str:
    if not parameter:
        full_url = url
    else:
        parameter_strings = []
        for key, value in parameter.items():
            parameter_strings.append(f'{key}={value}')
        full_url = f'{url}?{"&".join(parameter_strings)}'
    return full_url
