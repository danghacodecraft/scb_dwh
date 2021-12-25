import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

import json
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.employee.serializers import EmployeeResponseSerializer, BranchResponseSerializer, EmployeeKPIResponseSerializer, EmployeeWorkprocessResponseSerializer

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
            )
        ]
    )
    def emp_detail(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            emp_id = params['emp']

            # call the function
            sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_EMP_INFO(P_EMP=>'{}') FROM DUAL".format(emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    #[('03627', 'HỒ ĐỨC THẮNG', 'GIÁM ĐỐC PHÒNG QUẢN LÝ KHAI THÁC, PHÂN TÍCH DỮ LIỆU',
                    # '84', 'PHÒNG QUẢN LÝ KHAI THÁC, PHÂN TÍCH DỮ LIỆU',
                    # datetime.datetime(2010, 9, 6, 0, 0), 'THANGHD@SCB.COM.VN', '+84 907138520', '/var/www/EmployeeImage/03627.jpeg')]
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

            datas = []
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
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='EMP_DETAIL_PROFILE',
        summary='EMP_DETAIL_PROFILE',
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
    def emp_detail_profile(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            emp_id = params['emp']

            # call the function
            sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_EMP_WORKING_PROCESS('{}') FROM DUAL".format(emp_id)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            work_process = []
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

            datas = [
                {
                    "profile": {},
                    "contract": {},
                    "work_process": work_process
                }
            ]

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id='DEP_LIST',
        summary='DEP_LIST',
        tags=["EMPLOYEE"],
        responses={
            status.HTTP_201_CREATED: BranchResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `dep` example       
- **CAP_HOI_SO**.
- **CAP_VUNG**.
- **CAP_DVKD**.
""",
        parameters=[
            OpenApiParameter(
                name="dep", type=OpenApiTypes.STR, description="dep"
            )
        ]
    )
    def dep_list(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            dep = params['dep']

            # call the function
            sql = "SELECT obi.crm_dwh_pkg.FUN_GET_ORGANIZATION('ALL','{}', 'ALL') FROM DUAL".format(dep)
            print(sql)

            cur.execute(sql)
            res = cur.fetchone()

            ret = {}
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    print("Loi data ")
                    data_cursor = None

                for data in data_cursor:
                    print(data)
                    # (None, None, None, None, None, None, None, None, '001', 'SCB Cống Quỳnh', 'BAN GIAM DOC', '11838', 'Phòng Khách hàng Wholesale')
                    branch_id = data[8]
                    branch_name = data[9]

                    if branch_id not in ret:
                        ret[branch_id] = {
                            'branch_id': branch_id,
                            'branch_name': branch_name,
                            'director': data[10],
                            'departments': {}
                        }

                    departments = ret[branch_id]['departments']
                    department_id = data[11]
                    department_name = data[12]
                    if department_id != None and department_id not in departments:
                        departments[department_id] = {
                            'department_id': department_id,
                            'department_name': department_name
                        }

            cur.close()
            con.close()
            return self.response_success(ret, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

