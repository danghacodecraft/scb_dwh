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
                    # val = {
                    #     'id': lib.create_key(data[6].strip()),
                    #     "title": data[6].strip(),
                    #     'day': data[2],
                    #     'week': data[3],
                    #     'month': data[4],
                    #     'accumulated': data[5],
                    #     'unit': data[7]
                    # }
                    # datas.append(val)

            cur.close()
            con.close()
            return self.response_success( datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

