from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT


class ChartRequestSerializer(InheritedSerializer):
    module = serializers.CharField(help_text="`module` of chart")


class BranchRequestSerializer(InheritedSerializer):
    region = serializers.CharField(help_text="`region` of scb")


class RegionResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of region")
    title = serializers.CharField(help_text="`title` of region")


class BranchResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of branch")
    title = serializers.CharField(help_text="`title` of branch")


class ChartResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    title = serializers.CharField(help_text="`title` of data")
    val = serializers.IntegerField(help_text="`val` of data")
    unit = serializers.IntegerField(help_text="`unit` of data")

class DataResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    title = serializers.CharField(help_text="`title` of data")
    day = serializers.IntegerField(help_text="`day` of data")
    week = serializers.IntegerField(help_text="`week` of data")
    month = serializers.IntegerField(help_text="`month` of data")
    accumulated = serializers.IntegerField(help_text="`accumulated` of data")
