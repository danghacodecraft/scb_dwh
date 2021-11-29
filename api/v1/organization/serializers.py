from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

# class ChartRequestSerializer(InheritedSerializer):
#     module = serializers.CharField(help_text="`module` of chart")

class DataResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    title = serializers.CharField(help_text="`title` of data")
    day = serializers.IntegerField(help_text="`day` of data")
    week = serializers.IntegerField(help_text="`week` of data")
    month = serializers.IntegerField(help_text="`month` of data")
    accumulated = serializers.IntegerField(help_text="`accumulated` of data")
    unit = serializers.CharField(help_text="`unit` of data")
