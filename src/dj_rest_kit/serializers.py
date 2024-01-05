from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import helpers

User = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)

        # Adding this next line to the documented example
        read_only_fields = kwargs.pop("read_only_fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            existing = set(self.fields)
            for field_name in existing:
                if field_name in exclude:
                    self.fields.pop(field_name)

        # another bit we're adding to documented example, to take care of readonly fields
        if read_only_fields is not None:
            for f in read_only_fields:
                try:
                    self.fields[f].read_only = True
                except KeyError:
                    # not in fields anyway
                    pass

    @staticmethod
    def remove_null_key_value_pair(dictionary):
        return helpers.remove_null_key_value_pair(dictionary)

    @staticmethod
    def validate_float_value(value):
        try:
            return float(value)
        except ValueError:
            raise serializers.ValidationError("A valid number is required.")

    def unique_value_validator(
            self,
            field,
            value,
            error_message,
            look_up,
            check_parent_model=False,
            model=None,
            **kwargs,
    ):
        error_message = serializers.ValidationError(error_message)
        instance = self.instance
        model = self.Meta.model if not model else model
        if check_parent_model:
            model = model._meta.get_parent_list()[0]

        kwargs[look_up] = value

        if instance:
            if (
                    getattr(instance, field) != value
                    and model.objects.filter(**kwargs).exists()
            ):
                raise error_message
        elif model.objects.filter(**kwargs).exists():
            raise error_message
        return value


class DynamicFieldsUUIDModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    id = serializers.CharField(source="uuid", read_only=True)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)

        # Adding this next line to the documented example
        read_only_fields = kwargs.pop("read_only_fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsUUIDModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            existing = set(self.fields)
            for field_name in existing:
                if field_name in exclude:
                    self.fields.pop(field_name)

        # another bit we're adding to documented example, to take care of readonly fields
        if read_only_fields is not None:
            for f in read_only_fields:
                try:
                    self.fields[f].read_only = True
                except KeyError:
                    # not in fields anyway
                    pass

        for field_name, field in self.fields.items():
            if isinstance(field, serializers.ManyRelatedField):
                related_model = field.child_relation.queryset.model
                slug_related_field = serializers.SlugRelatedField(
                    slug_field="uuid",
                    required=False,
                    allow_null=True,
                    allow_empty=True,
                    queryset=related_model.objects.all(),
                    many=True,
                )
                self.fields[field_name] = slug_related_field
            elif isinstance(field, serializers.PrimaryKeyRelatedField):
                related_model = field.queryset.model
                slug_related_field = serializers.SlugRelatedField(
                    slug_field="uuid",
                    required=False,
                    allow_null=True,
                    allow_empty=True,
                    queryset=related_model.objects.all(),
                )
                self.fields[field_name] = slug_related_field

    @staticmethod
    def remove_null_key_value_pair(dictionary):
        return helpers.remove_null_key_value_pair(dictionary)

    @staticmethod
    def validate_float_value(value):
        try:
            return float(value)
        except ValueError:
            raise serializers.ValidationError("A valid number is required.")

    def unique_value_validator(
            self,
            field,
            value,
            error_message,
            look_up,
            check_parent_model=False,
            model=None,
            **kwargs,
    ):
        error_message = serializers.ValidationError(error_message)
        instance = self.instance
        model = self.Meta.model if not model else model
        if check_parent_model:
            model = model._meta.get_parent_list()[0]

        kwargs[look_up] = value

        if instance:
            if (
                    getattr(instance, field) != value
                    and model.objects.filter(**kwargs).exists()
            ):
                raise error_message
        elif model.objects.filter(**kwargs).exists():
            raise error_message
        return value


class ReadOnlyModelSerializer(DynamicFieldsModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            # set all field to read_only which eventually speed the response
            field.read_only = True
        return fields


class ReadOnlyUUIDModelSerializer(DynamicFieldsUUIDModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            # set all field to read_only which eventually speed the response
            field.read_only = True
        return fields
