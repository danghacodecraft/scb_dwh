from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

class EmployeeResponseSerializer(InheritedSerializer):
    emp_id = serializers.CharField(help_text="`emp_id` of data")
    emp_name = serializers.CharField(help_text="`emp_name` of data")
    title = serializers.CharField(help_text="`title` of data")
    dep_id = serializers.CharField(help_text="`dep_id` of data")
    dep_name = serializers.CharField(help_text="`dep_name` of data")
    time = serializers.CharField(help_text="`time` of data")
    email = serializers.CharField(help_text="`email` of data")
    mobile = serializers.CharField(help_text="`mobile` of data")
    avatar = serializers.CharField(help_text="`avatar` of data")


class BranchResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    fullname = serializers.CharField(help_text="`fullname` of data")
    level = serializers.CharField(help_text="`level` of data")
