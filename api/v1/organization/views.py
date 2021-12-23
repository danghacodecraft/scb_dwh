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
                # ('1', 'Ngân hàng TMCP Sài Gòn',
                # '4', 'Ban Điều hành',
                # '11422', 'Khối Phê duyệt Tín dụng và Xử lý nợ',
                # '13729', 'Trung tâm Thẩm định Tài sản',
                # '13736', 'Mảng Thẩm định Tài sản Hồ Chí Minh 2', None, None, None, None,
                # 'Mảng Thẩm định Tài sản Hồ Chí Minh 2', 'Mảng Thẩm định Tài sản Hồ Chí Minh 2', 'D8', 13736, 13729,
                # '1;4;11422;13729;13736;', 'Ngân hàng TMCP Sài Gòn;Ban Điều hành;Khối Phê duyệt Tín dụng và Xử lý nợ;Trung tâm Thẩm định Tài sản;Mảng Thẩm định Tài sản Hồ Chí Minh 2;', 7, datetime.datetime(2021, 9, 1, 0, 0))

                print(data)
                key1 = data[0]
                name1 = data[1]

                code = data[16]
                depid = str(data[17])

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

                        if name4 is not None and "Vùng" not in name4 and "Kênh" not in name4:
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
                                            'child': {},
                                            # 'code': code,
                                            # 'depid': depid
                                        }

                                    ret5 = ret4['child'][key5]
                                    if key5 == depid:
                                        ret5['code'] = code

                                    key6 = data[10]
                                    name6 = data[11]
                                    if key6 is not None:
                                        if key6 not in ret5['child']:
                                            ret5['child'][key6] = {
                                                'id': key6,
                                                'fullname': name6,
                                                'level': 6,
                                                'child': {},
                                                # 'code': code,
                                                # 'depid': depid
                                            }

                                        ret6 = ret5['child'][key6]
                                        if key6 == depid:
                                            ret6['code'] = code

                                    #     key7 = data[10]
                                    #     name7 = data[11]
                                    #     if key7 is not None:
                                    #         if key7 not in ret6['child']:
                                    #             ret6['child'][key7] = {
                                    #                 'id': key7,
                                    #                 'fullname': name7,
                                    #                 'level': 7,
                                    #                 'child': {}
                                    #             }

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

Param `type` example       
- **CAP_VUNG**.
""",
        parameters=[
            OpenApiParameter(
                name="name", type=OpenApiTypes.STR, description="name"
            ),
            OpenApiParameter(
                name="type", type=OpenApiTypes.STR, description="type"
            ),
            OpenApiParameter(
                name="userid", type=OpenApiTypes.STR, description="userid"
            )
        ]
    )
    def region(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()

            name = params['name']
            type = ", P_TYPE=>'CAP_VUNG'"
            if 'type' in params.keys():
                type = ", P_TYPE=>'{}'".format(params['type'])

            # userid = ", P_USER_ID=>'THANGHD'"
            # if 'userid' in params.keys():
            #     userid = ", P_USER_ID=>'{}'".format(params['userid'])

            # call the function
            sql = "Select obi.crm_dwh_pkg.FUN_GET_ORGANIZATION( P_REGION => '{}'{}) FROM DUAL".format(name, type)
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
                    # 'V02', 'Vùng 02', '015', 'SCB Quận 10', 'BAN GIAM DOC', None, None, '11986', 'Phòng Dịch vụ Khách hàng', None, None, '03')
                    region_id = data[6]
                    region_name = data[7]
                    if region_id not in ret:
                        ret[region_id] = {
                            'id': region_id,
                            'fullname': region_name,
                            'level': 1,
                            'child': {}
                        }

                    branch_childs = ret[region_id]['child']
                    branch_id = data[8]
                    branch_name = data[9]

                    if branch_id not in branch_childs:
                        branch_childs[branch_id] = {
                            'id': branch_id,
                            'fullname': branch_name,
                            'level': 2,
                            'child': {
                                branch_id: {
                                    'id': branch_id,
                                    'fullname': data[10],
                                    'level': 3,
                                    'child': {}
                                }
                            }
                        }

                    department_childs = branch_childs[branch_id]['child'][branch_id]['child']
                    department_id = data[13]
                    department_name = data[14]
                    code = data[17]
                    if department_id is not None and department_id not in department_childs:
                        department_childs[department_id] = {
                            'id': department_id,
                            'fullname': department_name,
                            'level': 4,
                            'child': {},
                            'code': code
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
        parameters=[
            OpenApiParameter(
                name="userid", type=OpenApiTypes.STR, description="userid"
            )
        ],
        responses={
            status.HTTP_201_CREATED: RegionResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def region_list(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()

            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'])

            sql = 'select obi.CRM_DWH_PKG.FUN_GET_REGION({}) FROM DUAL'.format(userid)
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

Param `type` example       
- **CAP_DVKD**.

""",
        parameters=[
            OpenApiParameter(
                name="name", type=OpenApiTypes.STR, description="name"
            ),
            OpenApiParameter(
                name="type", type=OpenApiTypes.STR, description="type"
            ),
            # OpenApiParameter(
            #     name="userid", type=OpenApiTypes.STR, description="userid"
            # ),
        ]
    )
    def branch(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            name = params['name']

            type = ", P_TYPE=>'CAP_DVKD'"
            if 'type' in params.keys():
                type = ", P_TYPE=>'{}'".format(params['type'])

            # userid = ", P_USER_ID=>'THANGHD'"
            # if 'userid' in params.keys():
            #     userid = ", P_USER_ID=>'{}'".format(params['userid'])

            # call the function
            sql = "Select obi.crm_dwh_pkg.FUN_GET_ORGANIZATION(P_BRANCH=>'{}'{}) FROM DUAL".format(name, type)
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
                            'id': branch_id,
                            'fullname': branch_name,
                            'level': 1,
                            'child': {
                                branch_id: {
                                    'id': branch_id,
                                    'fullname': data[10],
                                    'level': 2,
                                    'child': {}
                                }
                            }
                        }

                    department_childs = ret[branch_id]['child'][branch_id]['child']
                    department_id = data[13]
                    department_name = data[14]
                    code = data[17]
                    if department_id is not None and department_id not in department_childs:
                        department_childs[department_id] = {
                            'id': department_id,
                            'fullname': department_name,
                            'level': 3,
                            'child': {},
                            'code': code
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
                name="userid", type=OpenApiTypes.STR, description="userid"
            ),
            OpenApiParameter(
                name="type", type=OpenApiTypes.STR, description="type"
            ),
            OpenApiParameter(
                name="level", type=OpenApiTypes.STR, description="level"
            ),
        ]
    )
    def branch_list(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()

            userid = ", P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = ", P_USER_ID=>'{}'".format(params['userid'])

            type = ", P_TYPE=>'CAP_DVKD'"
            if 'type' in params.keys():
                type = ", P_TYPE=>'{}'".format(params['type'])

            flevel = ""
            if 'level' in params.keys():
                flevel = params['level']

            # call the function
            sql = "Select obi.crm_dwh_pkg.FUN_GET_BRANCH(P_VUNG=>'ALL'{}{}) FROM DUAL".format(userid, type)
            print(sql)
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
                    print(data)
                    id = data[0]
                    fullname = data[1]
                    level = data[2]
                    if level is None:
                        continue

                    if flevel != "" and flevel != level:
                        continue

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
