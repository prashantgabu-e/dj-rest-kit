import re

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .constants import FileFieldConstants


def image_size(value):
    limit = FileFieldConstants.IMAGE_SIZE
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 2 MB.")


def document_size(value):
    limit = FileFieldConstants.DOCUMENT_SIZE
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 10 MB.")


def no_past_date(value):
    today = timezone.now().date()
    if value < today:
        raise ValidationError("Date cannot be in the past.")


def no_past_date_time(value):
    today = timezone.now()
    if value < today:
        raise ValidationError("Datetime cannot be in the past.")


def time_validator(time):
    """time validator for 24 hours. validate HH:mm:ss time format"""
    if not time:
        return False

    return bool(re.match("^(2[0-3]|[01]?[0-9]):([0-5]?[0-9](:[0-5][0-9])?)$", time))
