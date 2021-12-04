import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

import json
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.organization.serializers import DataResponseSerializer

class OrganizationView(BaseAPIView):
    @extend_schema(
        operation_id='Data',
        summary='List',
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
        summary='List',
        tags=["ORGANIZATION"],
        description='Get region',
        responses={
            status.HTTP_201_CREATED: DataResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
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
                SELECT OBI.CRM_DWH_PKG.FUN_GET_ORGANIZATION(P_VUNG=>'{}',P_TYPE=>'CAP_VUNG') FROM DUAL
            """.format(name)
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

                    # ('11440', 'Vùng 05', '11589', 'SCB Tân Bình', 'BAN GIAM DOC', None, None)


                # key1 = data[0]
                # name1 = data[1]
                # if key1 not in ret:
                #     ret[key1] = {
                #         'id': key1,
                #         'fullname': name1,
                #         'level': 1,
                #         'child': {}
                #     }
                #
                # ret1 = ret[key1]
                # key2 = data[2]
                # name2 = data[3]
                # if key2 is not None:
                #     if key2 not in ret1['child']:
                #         ret1['child'][key2] = {
                #             'id': key2,
                #             'fullname': name2,
                #             'level': 2,
                #             'child': {}
                #         }
                #
                #     ret2 = ret1['child'][key2]
                #     key3 = data[4]
                #     name3 = data[5]
                #     if key3 is not None:
                #         if key3 not in ret2['child']:
                #             ret2['child'][key3] = {
                #                 'id': key3,
                #                 'fullname': name3,
                #                 'level': 3,
                #                 'child': {}
                #             }
                #
                #         ret3 = ret2['child'][key3]
                #         key4 = data[6]
                #         name4 = data[7]
                #         if key4 is not None:
                #             if key4 not in ret3['child']:
                #                 ret3['child'][key4] = {
                #                     'id': key4,
                #                     'fullname': name4,
                #                     'level': 4,
                #                     'child': {}
                #                 }
                #
                #             ret4 = ret3['child'][key4]
                #             key5 = data[8]
                #             name5 = data[9]
                #             if key5 is not None:
                #                 if key5 not in ret4['child']:
                #                     ret4['child'][key5] = {
                #                         'id': key5,
                #                         'fullname': name5,
                #                         'level': 5,
                #                         'child': {}
                #                     }
                #
                #                 ret5 = ret4['child'][key5]
                #                 key6 = data[10]
                #                 name6 = data[11]
                #                 if key6 is not None:
                #                     if key6 not in ret5['child']:
                #                         ret5['child'][key6] = {
                #                             'id': key6,
                #                             'fullname': name6,
                #                             'level': 6,
                #                             'child': {}
                #                         }
                #
                #                     ret6 = ret5['child'][key6]
                #                     key7 = data[10]
                #                     name7 = data[11]
                #                     if key7 is not None:
                #                         if key7 not in ret6['child']:
                #                             ret6['child'][key7] = {
                #                                 'id': key7,
                #                                 'fullname': name7,
                #                                 'level': 7,
                #                                 'child': {}
                #                             }

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Branch',
        summary='List',
        tags=["ORGANIZATION"],
        description='Get Branch',
        responses={
            status.HTTP_201_CREATED: DataResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
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
                SELECT OBI.CRM_DWH_PKG.FUN_GET_ORGANIZATION(P_BRANCH=>'{}',P_TYPE=>'CAP_DVKD') FROM DUAL
            """.format(name)
            print(sql)
            cur.execute(sql)
            datas = cur.fetchall()

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

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)