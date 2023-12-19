from django_filters import BaseInFilter, NumberFilter
from django_filters import rest_framework as filters
from django_filters.filters import OrderingFilter


class BaseFilter(filters.FilterSet):
    order_by_field = "ordering"


class BaseOrderingFilter(OrderingFilter):
    pass


class BaseNumberInFilter(BaseInFilter, NumberFilter):
    pass
