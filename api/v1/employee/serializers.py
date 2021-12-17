from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

# class ChartRequestSerializer(InheritedSerializer):
#     module = serializers.CharField(help_text="`module` of chart")

class DataResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    parent_id = serializers.CharField(help_text="`parent_id` of data")
    fullname = serializers.CharField(help_text="`fullname` of data")
    level = serializers.IntegerField(help_text="`level` of data")

class BranchResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    fullname = serializers.CharField(help_text="`fullname` of data")
    level = serializers.CharField(help_text="`level` of data")


class RegionResponseSerializer(InheritedSerializer):
    region_id = serializers.IntegerField(help_text="`id` of region")
    region_name = serializers.CharField(help_text="`name` of region")