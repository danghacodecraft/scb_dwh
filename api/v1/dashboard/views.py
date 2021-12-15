import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

import json
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.dashboard.serializers import DataResponseSerializer, ChartResponseSerializer


class DashboardView(BaseAPIView):
    @extend_schema(
        operation_id='Data',
        summary='List',
        tags=["Dashboard"],
        description="""
The `vung` example: 
- **V02**.

The `dv` example: 
- **001**.

""",
        parameters=[
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            )
        ],
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
            params = request.query_params.dict()
            vung = ""
            if 'vung' in params.keys():
                vung = ", p_vung=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ", p_dv=>'{}'".format(params['dv'])

            # call the function
            sql = "Select obi.CRM_DWH_PKG.FUN_GET_DATA('TRANG_CHU'{}{}) FROM DUAL".format(vung, dv)
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
                        'id': lib.create_key(data[6].strip()),
                        "title": data[6].strip(),
                        'day': data[2],
                        'week': data[3],
                        'month': data[4],
                        'accumulated': data[5],
                        'unit': data[7]
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success( datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Chart',
        summary='List',
        tags=["Dashboard"],
        description="""
The `module` has values: 
- **tong_so_but_toan**.
- **thu_phi_dich_vu**.
- **tang_truong_huy_dong**.

The `vung` example: 
- **V02**.

The `dv` example: 
- **001**.

""",
        parameters=[
            OpenApiParameter(
                name="module", type=OpenApiTypes.STR, description="module"
            ),
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            )
        ],
        # request=ChartRequestSerializer,
        responses={
            status.HTTP_201_CREATED: ChartResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            module = params['module']

            vung = ""
            if 'vung' in params.keys():
                vung = ", p_vung=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ", p_dv=>'{}'".format(params['dv'])

            # page_number = 1
            # if 'page_number' in params.keys():
            #     page_number = int(params['page_number'])
            # call the function
            sql = """
            Select obi.CRM_DWH_PKG.FUN_GET_CHART(
                P_MAN_HINH=>'TRANG_CHU',P_MODULE=>'{}'{}{}
            ) FROM DUAL""".format(module, vung, dv)
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
                        'id': lib.create_key(data[1].strip()),
                        'title': data[3].strip(),
                        'val': data[2],
                        'unit': data[4].strip()
                        # 'week': data[3],
                        # 'month': data[4],
                        # 'accumulated': data[5]
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

