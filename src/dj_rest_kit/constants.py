

class FieldConstants:
    NON_FIELD_ERRORS = "non_field_errors"


class DateTimeFormat:
    DATE = "%d-%m-%Y"
    DATE_TIME = "%Y-%m-%d %H:%M"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"
    FULL_DATE_TIME = "%d-%m-%Y %H:%M:%S"
    MULTIPLE_DATE_FORMATS = ("%m/%d/%Y", "%m-%d-%Y", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d")
    TIME = "%H:%M"


class FileFieldConstants:
    IMAGE_SIZE = 2 * 1024 * 1024
    DOCUMENT_SIZE = 10 * 1024 * 1024
    IMAGE_FORMATS = ["png", "jpg", "jpeg", "svg", "webp"]
    DOCUMENT_FORMATS = ["doc", "docx", "pdf", "xlsx", "xls", "csv"]
    VIDEO_FORMATS = ["mp4"]
    AUDIO_FORMATS = ["mp3", "aac", "wav"]
    IMAGE_PDF_FORMATS = IMAGE_FORMATS + ["pdf"]
    ATTACHMENT_FORMATS = IMAGE_FORMATS + DOCUMENT_FORMATS


class DjangoAdminConstants:
    default_list_fields = ["created", "modified"]


class Method:
    GET = "get"
    HEAD = "head"
    OPTIONS = "options"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"
    LIST = "list"
