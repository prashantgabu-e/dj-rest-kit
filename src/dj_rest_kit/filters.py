from django.db.models import ForeignKey, OneToOneField, ManyToManyField
from django_filters import BaseInFilter, NumberFilter, UUIDFilter
from django_filters import rest_framework as filters
from django_filters.filters import OrderingFilter


class BaseFilter(filters.FilterSet):
    order_by_field = "ordering"


class BaseOrderingFilter(OrderingFilter):
    pass


class BaseNumberInFilter(BaseInFilter, NumberFilter):
    pass


class BaseUUIDModelFilter(BaseFilter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.filters.items():
            if isinstance(field.field, (ForeignKey, OneToOneField, ManyToManyField)):
                self.filters[field_name] = UUIDFilter(field_name=field_name)
