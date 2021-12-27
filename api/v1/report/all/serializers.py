from rest_framework import serializers

from api.base.serializers import InheritedSerializer
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT

class ChartResponseSerializer(InheritedSerializer):
    CHITIEU = serializers.CharField(help_text="`CHITIEU` of data")
    SODU_DS_LK_KYT = serializers.CharField(help_text="`SODU_DS_LK_KYT` of data")
    THUC_HIEN_KY_T = serializers.CharField(help_text="`THUC_HIEN_KY_T` of data")
    KE_HOACH_KY_T = serializers.CharField(help_text="`KE_HOACH_KY_T` of data")
    TYLE_KY_T = serializers.CharField(help_text="`TYLE_KY_T` of data")
    THUC_HIEN_LK = serializers.CharField(help_text="`THUC_HIEN_LK` of data")
    KE_HOACH_LK = serializers.CharField(help_text="`KE_HOACH_LK` of data")
    TY_LY_LK = serializers.CharField(help_text="`TY_LY_LK` of data")
    DIEM_CHI_TIEU_LK = serializers.CharField(help_text="`DIEM_CHI_TIEU_LK` of data")
    DIEM_KH_LK = serializers.CharField(help_text="`DIEM_KH_LK` of data")
    KH_NAM = serializers.CharField(help_text="`KH_NAM` of data")
    TY_LE_NAM = serializers.CharField(help_text="`TY_LE_NAM` of data")
    DIEM_CHI_TIEU_KH_NAM = serializers.CharField(help_text="`DIEM_CHI_TIEU_KH_NAM` of data")
    DIEM_KH_NAM = serializers.CharField(help_text="`DIEM_KH_NAM` of data")
    AMOUNT_CHART = serializers.CharField(help_text="`AMOUNT_CHART` of data")