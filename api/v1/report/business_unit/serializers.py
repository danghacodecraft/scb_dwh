from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

class ChartFResponseSerializer(InheritedSerializer):
    TIEU_DE = serializers.CharField(help_text="`TIEU_DE` of data")
    CO_TSDB = serializers.CharField(help_text="`CO_TSDB` of data")
    UNIT = serializers.CharField(help_text="`UNIT` of data")
    BR = serializers.CharField(help_text="`BR` of data")
    KH = serializers.CharField(help_text="`KH` of data")
    DU_NO = serializers.CharField(help_text="`DU_NO` of data")
    DU_NO_XAU = serializers.CharField(help_text="`DU_NO_XAU` of data")
    DU_NO_QUA_HAN = serializers.CharField(help_text="`DU_NO_QUA_HAN` of data")
    TY_LE_DU_NO_XAU = serializers.CharField(help_text="`TY_LE_DU_NO_XAU` of data")
    TY_LE_DU_NO_QUA_HAN = serializers.CharField(help_text="`TY_LE_DU_NO_QUA_HAN` of data")
    TY_LE_DU_NO = serializers.CharField(help_text="`TY_LE_DU_NO` of data")
    PROGRAM_ID = serializers.CharField(help_text="`PROGRAM_ID` of data")
    USING_DETAIL = serializers.CharField(help_text="`USING_DETAIL` of data")


class DataResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    title = serializers.CharField(help_text="`title` of data")
    day = serializers.IntegerField(help_text="`day` of data")
    week = serializers.IntegerField(help_text="`week` of data")
    month = serializers.IntegerField(help_text="`month` of data")
    accumulated = serializers.IntegerField(help_text="`accumulated` of data")
    unit = serializers.CharField(help_text="`unit` of data")
    branch = serializers.CharField(help_text="`branch` of data")


class CustomerResponseSerializer(InheritedSerializer):
    MA_KH = serializers.CharField(help_text="`MA_KH` of data")
    TEN_KH = serializers.CharField(help_text="`TEN_KH` of data")
    GIAY_TO_DINH_DANH = serializers.CharField(help_text="`GIAY_TO_DINH_DANH` of data")
    DIA_CHI = serializers.CharField(help_text="`DIA_CHI` of data")
    DIEN_THOAI = serializers.CharField(help_text="`DIEN_THOAI` of data")
    EMAIL = serializers.CharField(help_text="`EMAIL` of data")
    HANG_KHACH_HANG = serializers.CharField(help_text="`HANG_KHACH_HANG` of data")
    TONG_TAI_SAN = serializers.IntegerField(help_text="`TONG_TAI_SAN` of data")
    TGCKH = serializers.IntegerField(help_text="`TGCKH` of data")
    TGTT = serializers.IntegerField(help_text="`TGTT` of data")
    TGKKH = serializers.IntegerField(help_text="`TGKKH` of data")
    THE_TIN_DUNG = serializers.IntegerField(help_text="`THE_TIN_DUNG` of data")
    DU_NO_VAY = serializers.IntegerField(help_text="`DU_NO_VAY` of data")
    NV_QL_MA = serializers.CharField(help_text="`NV_QL_MA` of data")
    NV_QL_TEN = serializers.CharField(help_text="`NV_QL_TEN` of data")
    NV_QL_EMAIL = serializers.CharField(help_text="`NV_QL_EMAIL` of data")
    NV_QL_SO_DT = serializers.CharField(help_text="`NV_QL_SO_DT` of data")

class RegionInfoResponseSerializer(InheritedSerializer):
    address = serializers.CharField(help_text="`address` of data")
    fullname = serializers.CharField(help_text="`fullname` of data")
    email = serializers.CharField(help_text="`email` of data")
    mobile = serializers.CharField(help_text="`mobile` of data")
    fullname_op = serializers.CharField(help_text="`fullname_op` of data")
    email_op = serializers.CharField(help_text="`email_op` of data")
    mobile_op = serializers.CharField(help_text="`mobile_op` of data")
