from django.contrib.postgres.fields.array import ArrayField
from django.db.models import CharField
from django.utils.encoding import force_str
from rest_framework import permissions, status
from rest_framework.response import Response


class ViewSetMixin:
    permission_classes = (permissions.IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.name)

    @staticmethod
    def custom_error_response(
            error_message, response_status=status.HTTP_400_BAD_REQUEST
    ):
        if isinstance(error_message, dict):
            error_response = error_message
        elif isinstance(error_message, list):
            error_response = {"non_field_errors": error_message}
        else:
            error_response = {"non_field_errors": [error_message]}
        return Response(error_response, status=response_status)

    @classmethod
    def get_choices_for_model_fields(cls, model):
        parsed_choices = {}
        for field in model._meta.get_fields():
            if (
                    isinstance(field, CharField)
                    and field.choices
                    or isinstance(field, ArrayField)
            ):
                field_choices = field.choices
                if isinstance(field, ArrayField) and isinstance(
                        field.base_field, CharField
                ):
                    field_choices = field.base_field.choices
                parsed_choices[field.name] = [
                    {
                        "value": choice_value,
                        "display_name": force_str(choice_name, strings_only=True),
                    }
                    for choice_value, choice_name in dict(field_choices).items()
                ]
        return parsed_choices
