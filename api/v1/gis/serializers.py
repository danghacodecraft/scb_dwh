from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

# class BranchRequestSerializer(InheritedSerializer):
#     region = serializers.CharField(help_text="`region` of branch")

class BranchResponseSerializer(InheritedSerializer):
    region_id = serializers.IntegerField(help_text="`region_id` of branch")
    region_name = serializers.IntegerField(help_text="`region_name` of branch")
    branch_id = serializers.IntegerField(help_text="`id` of branch")
    branch_name = serializers.CharField(help_text="`name` of branch")
    latitude = serializers.FloatField(help_text="`latitude` of branch")
    longitude = serializers.FloatField(help_text="`longitude` of branch")

class RegionResponseSerializer(InheritedSerializer):
    region_id = serializers.IntegerField(help_text="`id` of region")
    region_name = serializers.CharField(help_text="`name` of region")
