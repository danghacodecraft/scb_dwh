from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

# class ChartRequestSerializer(InheritedSerializer):
#     module = serializers.CharField(help_text="`module` of chart")

class ChartResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    title = serializers.CharField(help_text="`title` of data")
    val = serializers.IntegerField(help_text="`val` of data")
    unit = serializers.CharField(help_text="`unit` of data")

class DataResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    title = serializers.CharField(help_text="`title` of data")
    day = serializers.FloatField(help_text="`day` of data")
    week = serializers.FloatField(help_text="`week` of data")
    month = serializers.FloatField(help_text="`month` of data")
    accumulated = serializers.FloatField(help_text="`accumulated` of data")
    unit = serializers.CharField(help_text="`unit` of data")
    amt_year = serializers.FloatField(help_text="`amt_year` of data")
    amt_ky_truoc = serializers.FloatField(help_text="`amt_ky_truoc` of data")
