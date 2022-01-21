import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

import json
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.employee.serializers import EmployeeBonusResponseSerializer, EmployeeDisciplineResponseSerializer, EmployeeTrainingResponseSerializer, EmployeeResponseSerializer, EmployeeDecisionResponseSerializer, EmployeeKPIResponseSerializer, EmployeeWorkprocessResponseSerializer

class EmployeeView(BaseAPIView):
    @extend_schema(
        operation_id='EMP_LIST',
        summary='EMP_LIST',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `depid` example       
- **84**.

Param `type` example       
- **TONG_HOP**.
- **CAP_HOI_SO**.
- **CAP_VUNG**.
- **CAP_DVKD**.
""",
        parameters=[
            OpenApiParameter(
                name="orgid", type=OpenApiTypes.STR, description="orgid"
            ),
            OpenApiParameter(
                name="depid", type=OpenApiTypes.STR, description="depid"
            ),
            OpenApiParameter(
                name="type", type=OpenApiTypes.STR, description="type"
            )
        ]
    )
    def emp_list(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()

            type = "P_TYPE=>'TONG_HOP'"
            if 'type' in params.keys():
                type = "P_TYPE=>'{}'".format(params['type'])

            code = ""
            if 'orgid' in params.keys():
                code = ", P_ORG_ID=>'{}'".format(params['orgid'])
            elif 'depid' in params.keys():
                code = ", P_DEP_ID=>'{}'".format(params['depid'])

            # call the function
            sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_EMP_INFO({}{}) FROM DUAL".format(type, code)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    #('06150', 'VÕ KHANG NINH', 'CHUYÊN VIÊN QUẢN LÝ DỮ LIỆU', '84', 'MẢNG QUẢN LÝ DỮ LIỆU', datetime.datetime(2015, 2, 26, 0, 0), 'NINHVK@SCB.COM.VN', '+84 969627333', '/var/www/EmployeeImage/06150.jpeg')
                    print(data)
                    val = {
                        'emp_id': data[0],
                        'emp_name': data[1],
                        'title': data[2],
                        'dep_id': data[3],
                        'dep_name': data[4],
                        'time': str(data[5]),
                        'email': data[6],
                        'mobile': data[7],
                        'avatar': data[8],
                        'block_id': data[9],
                        'block_name': data[10],
                        'sex': data[11],
                        'branch_code': data[12],
                        'manager': data[13],
                        'working_processes': []
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL',
        summary='EMP_DETAIL',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `emp` example       
- **17889**.

""",
        parameters=[
            OpenApiParameter(
                name="emp", type=OpenApiTypes.STR, description="emp"
            ),
            OpenApiParameter(
                name="dep", type=OpenApiTypes.STR, description="dep"
            )
        ]
    )
    def emp_detail(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            sql = ""
            if 'emp' in params.keys():
                sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_EMP_INFO(P_EMP=>'{}') FROM DUAL".format(params['emp'])
            else:
                sql = "SELECT OBI.crm_dwh_pkg.FUN_GET_EMP_INFO(P_EMP=>'ALL', P_TYPE=>'BRN_MANA_INFO', P_DEP_ID=>'{}', P_ORG_ID=>'ALL') FROM DUAL".format(params['dep'])

            # call the function
            # sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_EMP_INFO(P_EMP=>'{}') FROM DUAL".format(emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            data = {}
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    #[('03627', 'HỒ ĐỨC THẮNG', 'GIÁM ĐỐC PHÒNG QUẢN LÝ KHAI THÁC, PHÂN TÍCH DỮ LIỆU',
                    # '84', 'PHÒNG QUẢN LÝ KHAI THÁC, PHÂN TÍCH DỮ LIỆU',
                    # datetime.datetime(2010, 9, 6, 0, 0), 'THANGHD@SCB.COM.VN', '+84 907138520', '/var/www/EmployeeImage/03627.jpeg')]
                    data = {
                        'emp_id': data[0],
                        'emp_name': data[1],
                        'title': data[2],
                        'dep_id': data[3],
                        'dep_name': data[4],
                        'time': str(data[5]),
                        'email': data[6],
                        'mobile': data[7],
                        'avatar': data[8],
                        'block_id': data[9],
                        'block_name': data[10],
                        'sex': data[11],
                        'branch_code': data[12],
                        'manager': data[13],
                        'nhom_nv': data[24],
                        'org_id': data[76],
                        'profile': {
                            'work': {
                                'cur':{
                                    'branch_code': data[14],
                                    'branch_name': data[15],
                                    'job_title_code': data[16],
                                    'job_title_name': data[2],
                                },
                                'org':{
                                    'branch_code': data[17],
                                    'branch_name': data[18],
                                    'job_title_code': data[19],
                                    'job_title_name': data[20],
                                },
                                'card_no': data[21],
                                'thu_viec': data[22],
                                'chinh_thuc': data[23],
                                'resident_status': data[77],
                            },
                            'contract': {
                                'type': data[32],
                                'name': data[33],
                                'start_date': data[34],
                                'end_date': data[35],
                            },
                            'work_process': []
                        },
                        'curriculum_vitae': {
                            'individual': {
                                'birth_date': data[59],
                                'birth_province': data[60],
                                'gender': data[61],
                                'native': data[62],
                                'religion': data[63],
                                'nationality': data[64],
                                'marital': data[65],
                                'passport': {
                                    'id': data[66],
                                    'issue_date': data[67],
                                    'expire_date': data[68],
                                    'issue_place': data[69]
                                }
                            },
                            'contact': {
                                'temp': {
                                    'address': data[36],
                                    'nation': data[37],
                                    'province': data[38],
                                    'ward': data[39],
                                    'district': data[40],
                                },
                                'per': {
                                    'address': data[41],
                                    'nation': data[42],
                                    'province': data[43],
                                    'ward': data[44],
                                    'district': data[45],
                                },
                                'nav': {
                                    'address': data[46],
                                    'nation': data[47],
                                    'province': data[48],
                                    'ward': data[49],
                                    'district': data[50],
                                },
                                'contact': {
                                    'address': data[51],
                                    'nation': data[52],
                                    'province': data[53],
                                    'ward': data[54],
                                    'district': data[55],
                                },
                                'family': {
                                    'name': data[56],
                                    'relation': data[57],
                                    'phone': data[58],

                                }
                            }
                        },
                        'level': {
                            'cultural': {
                                'academy': data[70],
                                'education_level': data[71],
                                'major': data[72],
                                'degree': data[73],
                                'school': data[74],
                                'training': data[75]
                            },
                            'foreign_language': {
                                'certificate': data[81],
                                'level': data[82],
                                'mark': data[83],
                            },
                            'information_technology': {
                                'certificate': data[78],
                                'level': data[79],
                                'mark': data[80],
                            }
                        }
                    }

            cur.close()
            con.close()
            return self.response_success(data, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL_KPI',
        summary='EMP_DETAIL_KPI',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeKPIResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `emp` example       
- **17889**.
- **14856**
""",
        parameters=[
            OpenApiParameter(
                name="emp", type=OpenApiTypes.STR, description="emp"
            )
        ]
    )
    def emp_detail_kpi(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            emp_id = params['emp']

            # call the function
            sql = "SELECT obi.crm_dwh_pkg.FUN_GET_EMP_KPI(P_EMP_CODE=>'{}') from dual".format(emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            kpis = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    # ('14856', 'Nguyễn Thị Xuân Nguyên', 480, '77.42%', 'Không đạt KPIs', '10/2021', None)
                    val = {
                        'ID': data[0],
                        'FULLNAME': data[1],
                        'KPI': data[2],
                        'PER': data[3],
                        'RES': data[4],
                        'DATE': data[5],
                        'NOTE': data[6]
                    }
                    kpis.append(val)

            cur.close()
            con.close()
            return self.response_success(kpis, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL_DECISION',
        summary='EMP_DETAIL_DECISION',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeDecisionResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `emp` example       
- **04260**.
""",
        parameters=[
            OpenApiParameter(
                name="emp", type=OpenApiTypes.STR, description="emp"
            )
        ]
    )
    def emp_detail_decision(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            emp_id = params['emp']

            # call the function
            sql = "SELECT obi.crm_dwh_pkg.FUN_GET_EMP_DECISION(P_EMP=>'{}') from dual".format(emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    #('04260', 'BÙI THỊ NHƯ QUỲNH', '000', 'MẢNG KẾ TOÁN CHI TIÊU NỘI BỘ TẬP TRUNG', None, '4894-4897/QĐ-TGĐ.16-Vi phạm An toàn kho quỹ', datetime.datetime(2016, 12, 14, 0, 0))

                    val = {
                        'ID': lib.parseString(data[0]),
                        'FULLNAME': lib.parseString(data[1]),
                        'DEP_ID': lib.parseString(data[2]),
                        'DEP_NAME': lib.parseString(data[3]),
                        'REASON_COMMEND': lib.parseString(data[4]),
                        'REASON_DISCIPLINE': lib.parseString(data[5]),
                        'DATETIME': lib.parseString(data[6])
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL_BONUS',
        summary='EMP_DETAIL_BONUS',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeBonusResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `emp` example       
- **05645**.
""",
        parameters=[
            OpenApiParameter(
                name="emp", type=OpenApiTypes.STR, description="emp"
            )
        ]
    )

    def emp_detail_bonus(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            emp_id = params['emp']

            # call the function
            sql = "SELECT obi.crm_dwh_pkg.FUN_GET_EMP_INFO(P_EMP=>'{}',P_TYPE=>'KHEN_THUONG',P_DEP_ID=>'ALL',P_ORG_ID=>'ALL') FROM DUAL".format(emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    # (datetime.datetime(2018, 3, 13, 0, 0), '971/QĐ-TGĐ.18', 'DHKT_3', 'CKT1', None, None, 'Khen thưởng các Cán bộ nhân viên đạt thành tích xuất sắc năm 2017', 'DHKT_3', 5000000, datetime.datetime(2018, 3, 13, 0, 0), 'VÕ TẤN HOÀNG VĂN')
                    val = {
                        'NGAY_HIEU_LUC': lib.parseString(data[0]),
                        'SO_QUYET_DINH': lib.parseString(data[1]),
                        'DANH_HIEU': lib.parseString(data[2]),
                        'CAP_KHEN_THUONG': lib.parseString(data[3]),
                        'CHUC_DANH': lib.parseString(data[4]),
                        'DON_VI_PHONG_BAN': lib.parseString(data[5]),
                        'LY_DO_KHEN_TUONG': lib.parseString(data[6]),
                        'HINH_THUC_KHEN_THUONG': lib.parseString(data[7]),
                        'SO_TIEN_THUONG': lib.parseString(data[8]),
                        'NGAY_KY': lib.parseString(data[9]),
                        'NGUOI_KY': lib.parseString(data[10])
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL_DISCIPLINE',
        summary='EMP_DETAIL_DISCIPLINE',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeDisciplineResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `emp` example       
- **08675**.
""",
        parameters=[
            OpenApiParameter(
                name="emp", type=OpenApiTypes.STR, description="emp"
            )
        ]
    )
    def emp_detail_discipline(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            emp_id = params['emp']

            # call the function
            sql = "SELECT obi.crm_dwh_pkg.FUN_GET_EMP_INFO(P_EMP=>'{}',P_TYPE=>'KY_LUAT',P_DEP_ID=>'ALL',P_ORG_ID=>'ALL') FROM DUAL".format(
                emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    # ('04260', 'BÙI THỊ NHƯ QUỲNH', '000', 'MẢNG KẾ TOÁN CHI TIÊU NỘI BỘ TẬP TRUNG', None, '4894-4897/QĐ-TGĐ.16-Vi phạm An toàn kho quỹ', datetime.datetime(2016, 12, 14, 0, 0))

                    val = {
                        'NGAY_HIEU_LUC': lib.parseString(data[0]),
                        'NGAY_KET_THUC': lib.parseString(data[1]),
                        'CHUC_DANH': lib.parseString(data[2]),
                        'DON_VI_PHONG_BAN': lib.parseString(data[3]),
                        'LY_DO_KY_LUAT': lib.parseString(data[4]),
                        'LY_DO_CHI_TIET_KY_LUAT': lib.parseString(data[5]),
                        'NGAY_PHAT_HIEN': lib.parseString(data[6]),
                        'NGAY_VI_PHAM': lib.parseString(data[7]),
                        'TONG_GIA_TRI_THIET_HAI': lib.parseString(data[8]),
                        'SO_QUYET_DINH': lib.parseString(data[9]),
                        'NGAY_XOA_KY_LUAT': lib.parseString(data[10]),
                        'NGUOI_KY': lib.parseString(data[11]),
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL_TRAINING',
        summary='EMP_DETAIL_TRAINING',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeTrainingResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `emp` example       
- **03626**.
""",
        parameters=[
            OpenApiParameter(
                name="emp", type=OpenApiTypes.STR, description="emp"
            )
        ]
    )
    def emp_detail_training(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            emp_id = params['emp']

            # call the function
            sql = "SELECT obi.crm_dwh_pkg.FUN_GET_EMP_INFO(P_EMP=>'{}',P_TYPE=>'DAO_TAO_NOI_BO',P_DEP_ID=>'ALL',P_ORG_ID=>'ALL') FROM DUAL".format(
                emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    # ('04260', 'BÙI THỊ NHƯ QUỲNH', '000', 'MẢNG KẾ TOÁN CHI TIÊU NỘI BỘ TẬP TRUNG', None, '4894-4897/QĐ-TGĐ.16-Vi phạm An toàn kho quỹ', datetime.datetime(2016, 12, 14, 0, 0))

                    val = {
                        'CHU_DE': lib.parseString(data[0]),
                        'MA_KHOA_HOC': lib.parseString(data[1]),
                        'TEN_KHOA_HOC': lib.parseString(data[2]),
                        'TU_NGAY': lib.parseString(data[3]),
                        'DEN_NGAY': lib.parseString(data[4]),
                        'KET_QUA': lib.parseString(data[5])
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL_WORK_PROCESS',
        summary='EMP_DETAIL_WORK_PROCESS',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: EmployeeWorkprocessResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `emp` example       
- **17889**.
- **14856**
""",
        parameters=[
            OpenApiParameter(
                name="emp", type=OpenApiTypes.STR, description="emp"
            )
        ]
    )
    def emp_detail_work_process(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()
            emp_id = params['emp']

            work_process = []
            # =============================================
            sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_EMP_WORKING_PROCESS('{}') FROM DUAL".format(emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    val = {
                        'EMPLOYEE_CODE': data[0],
                        'TU_NGAY': data[1],
                        'DEN_NGAY': data[2],
                        'CONG_TY': data[3],
                        'CHUC_VU': data[4]
                    }
                    work_process.append(val)

            cur.close()
            con.close()
            return self.response_success(work_process, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


#     @extend_schema(
#         operation_id='DEP_LIST',
#         summary='DEP_LIST',
#         tags=["EMPLOYEE"],
#         responses={
#             status.HTTP_201_CREATED: BranchResponseSerializer(many=True),
#             status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
#             status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
#         },
#         description="""
# Param `dep` example
# - **CAP_HOI_SO**.
# - **CAP_VUNG**.
# - **CAP_DVKD**.
# """,
#         parameters=[
#             OpenApiParameter(
#                 name="dep", type=OpenApiTypes.STR, description="dep"
#             )
#         ]
#     )
#     def dep_list(self, request):
#         try:
#             con, cur = lib.connect()
#
#             params = request.query_params.dict()
#             dep = params['dep']
#
#             # call the function
#             sql = "SELECT obi.crm_dwh_pkg.FUN_GET_ORGANIZATION('ALL','{}', 'ALL') FROM DUAL".format(dep)
#             print(sql)
#
#             cur.execute(sql)
#             res = cur.fetchone()
#
#             ret = {}
#             if len(res) > 0:
#                 try:
#                     data_cursor = res[0]
#                 except:
#                     print("Loi data ")
#                     data_cursor = None
#
#                 for data in data_cursor:
#                     print(data)
#                     # (None, None, None, None, None, None, None, None, '001', 'SCB Cống Quỳnh', 'BAN GIAM DOC', '11838', 'Phòng Khách hàng Wholesale')
#                     branch_id = data[8]
#                     branch_name = data[9]
#
#                     if branch_id not in ret:
#                         ret[branch_id] = {
#                             'branch_id': branch_id,
#                             'branch_name': branch_name,
#                             'director': data[10],
#                             'departments': {}
#                         }
#
#                     departments = ret[branch_id]['departments']
#                     department_id = data[11]
#                     department_name = data[12]
#                     if department_id != None and department_id not in departments:
#                         departments[department_id] = {
#                             'department_id': department_id,
#                             'department_name': department_name
#                         }
#
#             cur.close()
#             con.close()
#             return self.response_success(ret, status_code=status.HTTP_200_OK)
#         except cx_Oracle.Error as error:
#             cur.close()
#             con.close()
#             return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

