import uuid

from django.db.models import (
    BooleanField,
    CharField,
    ForeignObjectRel,
    ManyToManyRel,
    OneToOneRel, UUIDField,
)
from model_utils.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    ORDERING = ("-created",)

    class Meta:
        abstract = True

    @classmethod
    def get_raw_id_fields(cls):
        raw_id_fields = []
        for field in cls._meta.get_fields():
            if any(
                    (
                            isinstance(field.remote_field, ForeignObjectRel),
                            isinstance(field.remote_field, ManyToManyRel),
                            isinstance(field.remote_field, OneToOneRel),
                    )
            ):
                raw_id_fields.append(field.name)
        return raw_id_fields

    @classmethod
    def get_all_field_names(cls):
        return [field.name for field in cls._meta.fields]

    @classmethod
    def get_list_filter_fields(cls, *args):
        list_filter = ["created", "modified"]
        exclude_fields = (arg for arg in args)
        for field in cls._meta.get_fields():
            if (
                    isinstance(field, BooleanField)
                    or (isinstance(field, CharField) and field.choices)
            ) and field.name not in exclude_fields:
                list_filter.append(field.name)
        return list_filter


class BaseUUIDModel(BaseModel):
    uuid = UUIDField(default=uuid.uuid4, db_index=True, unique=True)

    class Meta:
        abstract = True
