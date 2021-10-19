import json

from rest_framework import serializers


def custom_serializers_char_field():
    def new_to_internal_value(self, data):
        # DEFAULT CHAR FIELD
        # We're lenient with allowing basic numerics to be coerced into strings,
        # but other types should fail. Eg. unclear if booleans should represent as `true` or `True`,
        # and composites such as lists are likely user error.

        # CUSTOM CHAR FIELD
        # Only accept string
        if not isinstance(data, str):
            self.fail('invalid')
        value = str(data)
        return value.strip() if self.trim_whitespace else value

    serializers.CharField.to_internal_value = new_to_internal_value


# [IMPORTANT] Custom serializers.CharField: only accept str instead of str, int, float (default in Django REST)
custom_serializers_char_field()


def custom_serializers_json_field():
    def new_to_internal_value(self, data):
        # DEFAULT JSON FIELD
        # not raise exception when input is not json

        # CUSTOM CHAR FIELD
        # Only accept string
        if not isinstance(data, (dict, list)):
            self.fail('invalid')

        try:
            if self.binary or getattr(data, 'is_json_string', False):
                if isinstance(data, bytes):
                    data = data.decode()
                return json.loads(data, cls=self.decoder)
            else:
                json.dumps(data, cls=self.encoder)
        except (TypeError, ValueError):
            self.fail('invalid')
        return data

    serializers.JSONField.to_internal_value = new_to_internal_value


# [IMPORTANT] Custom serializers.JSONField: only accept json
custom_serializers_json_field()


class InheritedSerializer(serializers.Serializer):
    def create(self, validated_data):  # noqa
        pass

    def update(self, instance, validated_data):  # noqa
        pass


class EmptyRequestSerializer(InheritedSerializer):
    pass


class ExceptionResponseSerializer(InheritedSerializer):
    error_code = serializers.CharField(help_text="Unique code of this error")
    description = serializers.CharField(help_text="Detail description of this error")
