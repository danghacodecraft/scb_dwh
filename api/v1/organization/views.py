import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

import json
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.organization.serializers import DataResponseSerializer, BranchResponseSerializer, RegionResponseSerializer


def myRegion(e):
    return e['region_id']

class OrganizationView(BaseAPIView):
    @extend_schema(
        operation_id='Data',
        summary='Data',
        tags=["ORGANIZATION"],
        description='Get Data',
        responses={
            status.HTTP_201_CREATED: DataResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def data(self, request):
        try:
            con, cur = lib.connect()

            # print(cx_Oracle.version)
            # print("Database version:", con.version)
            # print("Client version:", cx_Oracle.clientversion())

            # call the function
            sql = """
                SELECT * 
                FROM OBI.dwhf_hr_organization 
                ORDER BY NVL(PARENT_ID,ID), ORDER_BY
            """
            print(sql)
            cur.execute(sql)
            datas = cur.fetchall()

            ret = {}
            for data in datas:
                key1 = data[0]
                name1 = data[1]
                if key1 not in ret:
                    ret[key1] = {
                        'id': key1,
                        'fullname': name1,
                        'level': 1,
                        'child': {}
                    }

                ret1 = ret[key1]
                key2 = data[2]
                name2 = data[3]
                if key2 is not None:
                    if key2 not in ret1['child']:
                        ret1['child'][key2] = {
                            'id': key2,
                            'fullname': name2,
                            'level': 2,
                            'child': {}
                        }

                    ret2 = ret1['child'][key2]
                    key3 = data[4]
                    name3 = data[5]
                    if key3 is not None:
                        if key3 not in ret2['child']:
                            ret2['child'][key3] = {
                                'id': key3,
                                'fullname': name3,
                                'level': 3,
                                'child': {}
                            }

                        ret3 = ret2['child'][key3]
                        key4 = data[6]
                        name4 = data[7]
                        if key4 is not None:
                            if key4 not in ret3['child']:
                                ret3['child'][key4] = {
                                    'id': key4,
                                    'fullname': name4,
                                    'level': 4,
                                    'child': {}
                                }

                            ret4 = ret3['child'][key4]
                            key5 = data[8]
                            name5 = data[9]
                            if key5 is not None:
                                if key5 not in ret4['child']:
                                    ret4['child'][key5] = {
                                        'id': key5,
                                        'fullname': name5,
                                        'level': 5,
                                        'child': {}
                                    }

                                ret5 = ret4['child'][key5]
                                key6 = data[10]
                                name6 = data[11]
                                if key6 is not None:
                                    if key6 not in ret5['child']:
                                        ret5['child'][key6] = {
                                            'id': key6,
                                            'fullname': name6,
                                            'level': 6,
                                            'child': {}
                                        }

                                    ret6 = ret5['child'][key6]
                                    key7 = data[10]
                                    name7 = data[11]
                                    if key7 is not None:
                                        if key7 not in ret6['child']:
                                            ret6['child'][key7] = {
                                                'id': key7,
                                                'fullname': name7,
                                                'level': 7,
                                                'child': {}
                                            }

            cur.close()
            con.close()
            return self.response_success(ret, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id='Region',
        summary='Region',
        tags=["ORGANIZATION"],
        responses={
            status.HTTP_201_CREATED: DataResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `name` example       
- **V01**.
""",
        parameters=[
            OpenApiParameter(
                name="name", type=OpenApiTypes.STR, description="name"
            ),
        ]
    )
    def region(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            name = params['name']

            # call the function
            sql = """
                select obi.crm_dwh_pkg.FUN_GET_ORGANIZATION(
                    P_REGION => '{}',P_TYPE=> 'CAP_VUNG'
                ) FROM DUAL
            """.format(name)
            print(sql)
            # SELECT
            # OBI.CRM_DWH_PKG.FUN_GET_ORGANIZATION(P_REGION= > '{}', P_TYPE = > 'CAP_VUNG') FROM
            # DUAL
            cur.execute(sql)
            res = cur.fetchone()
            datas = []


            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    print("Loi data ")
                    data_cursor = None

                ret = {}
                for data in data_cursor:
                    print(data)
                    # 'V01', 'Vùng 01', '161', 'SCB Nam Sài Gòn', 'BAN GIAM DOC', '11941', 'Phòng Dịch vụ Khách hàng')
                    # 'V02', 'Vùng 02', '015', 'SCB Quận 10', 'BAN GIAM DOC', None, None, '11986', 'Phòng Dịch vụ Khách hàng', None, None, '03')
                    region_id = data[6]
                    region_name = data[7]
                    if region_id not in ret:
                        ret[region_id] = {
                            'region_id': region_id,
                            'region_name': region_name,
                            'branchs': {}
                        }

                    branchs = ret[region_id]['branchs']
                    branch_id = data[8]
                    branch_name = data[9]

                    if branch_id not in branchs:
                        branchs[branch_id] = {
                            'branch_id': branch_id,
                            'branch_name': branch_name,
                            'director': data[10],
                            'departments': {}
                        }

                    departments = branchs[branch_id]['departments']
                    department_id = data[13]
                    department_name = data[14]
                    if department_id is not None and department_id not in departments:
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

    @extend_schema(
        operation_id='Region_List',
        summary='Region_List',
        tags=["ORGANIZATION"],
        description="Region List",
        responses={
            status.HTTP_201_CREATED: RegionResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def region_list(self, request):
        try:
            con, cur = lib.connect()

            sql = 'select obi.CRM_DWH_PKG.FUN_GET_REGION FROM DUAL'
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    print("Loi data ")
                    data_cursor = None

                for data in data_cursor:
                    print(data)
                    val = {
                        'region_id': data[0].strip(),
                        'region_name': data[1].strip()
                    }
                    datas.append(val)

                datas.sort(key=myRegion)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id='Branch',
        summary='Branch',
        tags=["ORGANIZATION"],
        responses={
            status.HTTP_201_CREATED: DataResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `name` example       
- **001**.
""",
        parameters=[
            OpenApiParameter(
                name="name", type=OpenApiTypes.STR, description="name"
            ),
        ]
    )
    def branch(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            name = params['name']

            # call the function
            sql = """
                select obi.crm_dwh_pkg.FUN_GET_ORGANIZATION(
                    P_BRANCH=>'{}', P_TYPE=>'CAP_DVKD'
                ) FROM DUAL
            """.format(name)
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
                    department_id = data[13]
                    department_name = data[14]
                    if department_id is not None and department_id not in departments:
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

    @extend_schema(
        operation_id='Branch_List',
        summary='Branch_List',
        tags=["ORGANIZATION"],
        responses={
            status.HTTP_201_CREATED: BranchResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        description="""
Param `type` example       
- **CAP_DVKD**.
""",
        parameters=[
            OpenApiParameter(
                name="type", type=OpenApiTypes.STR, description="type"
            ),
        ]
    )
    def branch_list(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            type = params['type']

            # call the function
            sql = """
                    select obi.crm_dwh_pkg.FUN_GET_BRANCH(P_VUNG => 'ALL',P_TYPE => '{}') FROM DUAL
                """.format(type)

            cur.execute(sql)
            res = cur.fetchone()
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    print("Loi data ")
                    data_cursor = None

                ret = {}
                for data in data_cursor:
                    id = data[0]
                    fullname = data[1]
                    level = data[2]

                    if level not in ret:
                        ret[level] = []

                    branchs = ret[level]
                    branchs.append({
                        'id': id,
                        'fullname': fullname
                    })

            cur.close()
            con.close()
            return self.response_success(ret, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
