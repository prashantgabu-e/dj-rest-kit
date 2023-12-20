from django.contrib import admin
from django.db.models import ForeignObjectRel, ManyToManyRel, OneToOneRel, BooleanField, CharField
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from . import constants


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "modified")
    raw_id_fields = ()
    list_filter = ()
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    list_display = constants.DjangoAdminConstants.default_list_fields

    def __init__(self, model, admin_site, *args, **kwargs):
        self.raw_id_fields = self.setup_raw_id_fields(model)
        self.list_filter = self.setup_list_filter_fields(model)
        self.list_display += constants.DjangoAdminConstants.default_list_fields
        super().__init__(model, admin_site, *args, **kwargs)

    def setup_raw_id_fields(self, model):
        raw_id_fields = []
        for field in model._meta.get_fields():
            if any((isinstance(field.remote_field, ForeignObjectRel), isinstance(field.remote_field, ManyToManyRel),
                    isinstance(field.remote_field, OneToOneRel))):
                raw_id_fields.append(field.name)
        return raw_id_fields

    def setup_list_filter_fields(self, model):
        list_filter = ["created", "modified"]
        for field in model._meta.get_fields():
            if (isinstance(field, BooleanField) or (
                    isinstance(field, CharField) and field.choices)) and field.name:
                list_filter.append(field.name)
        return list_filter
