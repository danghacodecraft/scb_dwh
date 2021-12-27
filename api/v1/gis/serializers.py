from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

# class BranchRequestSerializer(InheritedSerializer):
#     region = serializers.CharField(help_text="`region` of branch")

class BranchResponseSerializer(InheritedSerializer):
    region_id = serializers.CharField(help_text="`region_id` of branch")
    region_name = serializers.CharField(help_text="`region_name` of branch")
    area_id = serializers.CharField(help_text="`area_id` of branch")
    area_name = serializers.CharField(help_text="`area_name` of branch")
    branch_id = serializers.CharField(help_text="`id` of branch")
    branch_name = serializers.CharField(help_text="`name` of branch")
    latitude = serializers.FloatField(help_text="`latitude` of branch")
    longitude = serializers.FloatField(help_text="`longitude` of branch")
    type = serializers.CharField(help_text="`type` of branch")

class RegionResponseSerializer(InheritedSerializer):
    region_id = serializers.CharField(help_text="`id` of region")
    region_name = serializers.CharField(help_text="`name` of region")
    left = serializers.FloatField(help_text="`left` of branch")
    right = serializers.FloatField(help_text="`right` of branch")
    top = serializers.FloatField(help_text="`top` of branch")
    bottom = serializers.FloatField(help_text="`bottom` of branch")

class AreaResponseSerializer(InheritedSerializer):
    ID = serializers.CharField(help_text="`ID` of data")
    NAME = serializers.CharField(help_text="`NAME` of data")
    left = serializers.FloatField(help_text="`left` of branch")
    right = serializers.FloatField(help_text="`right` of branch")
    top = serializers.FloatField(help_text="`top` of branch")
    bottom = serializers.FloatField(help_text="`bottom` of branch")

class BranchAreaResponseSerializer(InheritedSerializer):
    ID = serializers.CharField(help_text="`ID` of data")
    NAME = serializers.CharField(help_text="`NAME` of data")
    latitude = serializers.FloatField(help_text="`latitude` of branch")
    longitude = serializers.FloatField(help_text="`longitude` of branch")
    KHU_VUC = serializers.CharField(help_text="`KHU_VUC` of branch")

