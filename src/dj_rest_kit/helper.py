import os
import random
from uuid import uuid4

import pytz
from dateutil import parser
from django.conf import settings

from . import constants


def get_response_message(data, model, action="create"):
    obj_response_message = data.get("response_message", None)
    response_message = f"{obj_response_message} {action}d successfully"
    return response_message


def remove_null_key_value_pair(dictionary):
    return {k: v for k, v in dictionary.items() if v not in [None, "", "N/A"]}


def get_absolute_url(request, field):
    if not field:
        return None
    return request.build_absolute_uri(field.url)


def format_date_time(input_date):
    if input_date:
        return input_date.strftime(constants.DateTimeFormat.DATE_TIME)
    return None


def format_date(input_date, date_format=constants.DateTimeFormat.DATE):
    if input_date:
        return input_date.strftime(date_format)
    return None


def format_time(input_time):
    if input_time:
        return input_time.strftime(constants.DateTimeFormat.TIME)
    return None


def get_bulk_upload_response_message(model, action="bulk_upload"):
    model_name = model._meta.verbose_name.title()
    response_message = f"{model_name} data uploaded successfully"
    return response_message


def generate_random_otp():
    return random.randint(100000, 999999)


def get_user_timezone_from_request(request):
    default_timezone = settings.TIME_ZONE
    if request:
        return request.headers.get("timezone", default_timezone)
    return default_timezone


def convert_to_utc(aware_date_time):
    date_time_utc = aware_date_time.astimezone(pytz.UTC)
    return date_time_utc


def convert_to_user_timezone(utc_date_time, request=None, user_timezone=None):
    """
    Converts the UTC date time to date time with user's timezone
    """
    if not user_timezone:
        user_timezone = get_user_timezone_from_request(request)
    user_timezone = pytz.timezone(user_timezone)
    date_time_user_timezone = utc_date_time.astimezone(user_timezone)
    return date_time_user_timezone


def convert_to_formatted_user_timezone(utc_date_time, request=None, user_timezone=None):
    """
    Converts the UTC date time to date time string with user's timezone
    """
    if not user_timezone:
        user_timezone = get_user_timezone_from_request(request)
    user_timezone = pytz.timezone(user_timezone)
    date_time_user_timezone = utc_date_time.astimezone(user_timezone)
    formatted_date_time_str = format_date_time(date_time_user_timezone)
    return formatted_date_time_str


def convert_user_datetime_str_to_utc(datetime_str, timezone_str):
    """
    Converts user given date time string to UTC date time
    """
    naive_datetime = parser.parse(datetime_str)
    timezone = pytz.timezone(timezone_str)
    aware_datetime = timezone.localize(naive_datetime)
    utc_datetime = convert_to_utc(aware_datetime)
    return utc_datetime


def path_and_rename(sub_path):
    """
    Returns a function that can be used as the `upload_to` parameter for Django ImageField or FileField.

    This function generates a new filename for uploaded files by appending a UUID to the
    original filename and placing it in the specified subdirectory path.
    """
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(sub_path, filename)

    return wrapper
