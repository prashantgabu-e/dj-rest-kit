from rest_framework import pagination


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 10

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request, total_count=self.count)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset: self.offset + self.limit])

    def get_limit(self, request, total_count=None):
        if request.query_params.get(self.limit_query_param) == "all":
            return total_count
        return super().get_limit(request=request)
