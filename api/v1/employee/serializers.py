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
    block_id = serializers.CharField(help_text="`block_id` of data")
    block_name = serializers.CharField(help_text="`block_name` of data")
    sex = serializers.CharField(help_text="`sex` of data")
    branch_code = serializers.CharField(help_text="`branch_code` of data")
    manager = serializers.CharField(help_text="`manager` of data")

class EmployeeKPIResponseSerializer(InheritedSerializer):
    ID = serializers.CharField(help_text="`ID` of data")
    FULLNAME = serializers.CharField(help_text="`FULLNAME` of data")
    KPI = serializers.CharField(help_text="`KPI` of data")
    PER = serializers.CharField(help_text="`PER` of data")
    RES = serializers.CharField(help_text="`RES` of data")
    DATE = serializers.CharField(help_text="`DATE` of data")
    NOTE = serializers.CharField(help_text="`NOTE` of data")

class EmployeeDecisionResponseSerializer(InheritedSerializer):
    ID = serializers.CharField(help_text="`ID` of data")
    FULLNAME = serializers.CharField(help_text="`FULLNAME` of data")
    DEP_ID = serializers.CharField(help_text="`KPI` of data")
    DEP_NAME = serializers.CharField(help_text="`PER` of data")
    REASON_COMMEND = serializers.CharField(help_text="`RES` of data")
    REASON_DISCIPLINE = serializers.CharField(help_text="`DATE` of data")
    DATETIME = serializers.CharField(help_text="`NOTE` of data")

class EmployeeBonusResponseSerializer(InheritedSerializer):
    NGAY_HIEU_LUC = serializers.CharField(help_text="`NGAY_HIEU_LUC` of data")
    SO_QUYET_DINH = serializers.CharField(help_text="`SO_QUYET_DINH` of data")
    DANH_HIEU = serializers.CharField(help_text="`DANH_HIEU` of data")
    CAP_KHEN_THUONG = serializers.CharField(help_text="`CAP_KHEN_THUONG` of data")
    CHUC_DANH = serializers.CharField(help_text="`CHUC_DANH` of data")
    DON_VI_PHONG_BAN = serializers.CharField(help_text="`DON_VI_PHONG_BAN` of data")
    LY_DO_KHEN_TUONG = serializers.CharField(help_text="`LY_DO_KHEN_TUONG` of data")
    HINH_THUC_KHEN_THUONG = serializers.CharField(help_text="`HINH_THUC_KHEN_THUONG` of data")
    SO_TIEN_THUONG = serializers.CharField(help_text="`SO_TIEN_THUONG` of data")
    NGAY_KY = serializers.CharField(help_text="`NGAY_KY` of data")
    NGUOI_KY = serializers.CharField(help_text="`NGUOI_KY` of data")

class EmployeeDisciplineResponseSerializer(InheritedSerializer):
    NGAY_HIEU_LUC = serializers.CharField(help_text="`NGAY_HIEU_LUC` of data")
    NGAY_KET_THUC = serializers.CharField(help_text="`NGAY_KET_THUC` of data")
    CHUC_DANH = serializers.CharField(help_text="`CHUC_DANH` of data")
    DON_VI_PHONG_BAN = serializers.CharField(help_text="`DON_VI_PHONG_BAN` of data")
    LY_DO_KY_LUAT = serializers.CharField(help_text="`LY_DO_KY_LUAT` of data")
    LY_DO_CHI_TIET_KY_LUAT = serializers.CharField(help_text="`LY_DO_CHI_TIET_KY_LUAT` of data")
    NGAY_PHAT_HIEN = serializers.CharField(help_text="`NGAY_PHAT_HIEN` of data")
    NGAY_VI_PHAM = serializers.CharField(help_text="`NGAY_VI_PHAM` of data")
    TONG_GIA_TRI_THIET_HAI = serializers.CharField(help_text="`TONG_GIA_TRI_THIET_HAI` of data")
    SO_QUYET_DINH = serializers.CharField(help_text="`SO_QUYET_DINH` of data")
    NGAY_XOA_KY_LUAT = serializers.CharField(help_text="`NGAY_XOA_KY_LUAT` of data")
    NGUOI_KY = serializers.CharField(help_text="`NGUOI_KY` of data")


class EmployeeTrainingResponseSerializer(InheritedSerializer):
    CHU_DE = serializers.CharField(help_text="`CHU_DE` of data")
    MA_KHOA_HOC = serializers.CharField(help_text="`MA_KHOA_HOC` of data")
    TEN_KHOA_HOC = serializers.CharField(help_text="`TEN_KHOA_HOC` of data")
    TU_NGAY = serializers.CharField(help_text="`TU_NGAY` of data")
    DEN_NGAY = serializers.CharField(help_text="`DEN_NGAY` of data")
    KET_QUA = serializers.CharField(help_text="`KET_QUA` of data")

class EmployeeOtherResponseSerializer(InheritedSerializer):
    EMPLOYEE_ID = serializers.CharField(help_text="`EMPLOYEE_ID` of data")
    MA_TUYEN_DUNG = serializers.CharField(help_text="`MA_TUYEN_DUNG` of data")
    LY_DO_TUYEN_DUNG = serializers.CharField(help_text="`LY_DO_TUYEN_DUNG` of data")
    NGUOI_GIOI_THIEU = serializers.CharField(help_text="`NGUOI_GIOI_THIEU` of data")
    MA_KHOA_HOC = serializers.CharField(help_text="`MA_KHOA_HOC` of data")
    NV_THAY_THE = serializers.CharField(help_text="`NV_THAY_THE` of data")
    NOTE = serializers.CharField(help_text="`NOTE` of data")
    THONG_TIN_KHAC = serializers.CharField(help_text="`THONG_TIN_KHAC` of data")
    THAM_NIEN_THEM = serializers.CharField(help_text="`THAM_NIEN_THEM` of data")
    PHEP_NAM_UU_DAI = serializers.CharField(help_text="`PHEP_NAM_UU_DAI` of data")

class EmployeeWorkprocessResponseSerializer(InheritedSerializer):
    EMPLOYEE_CODE = serializers.CharField(help_text="`EMPLOYEE_CODE` of data")
    TU_NGAY = serializers.CharField(help_text="`TU_NGAY` of data")
    DEN_NGAY = serializers.CharField(help_text="`DEN_NGAY` of data")
    CONG_TY = serializers.CharField(help_text="`CONG_TY` of data")
    CHUC_VU = serializers.CharField(help_text="`CHUC_VU` of data")

class BranchResponseSerializer(InheritedSerializer):
    id = serializers.CharField(help_text="`id` of data")
    fullname = serializers.CharField(help_text="`fullname` of data")
    level = serializers.CharField(help_text="`level` of data")


