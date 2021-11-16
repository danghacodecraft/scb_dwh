import cx_Oracle
import api.v1.function as lib

import json
from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.dashboard.serializers import DataResponseSerializer, \
    ChartRequestSerializer, ChartResponseSerializer


class DashboardView(BaseAPIView):
    @extend_schema(
        operation_id='Data',
        summary='List',
        tags=["Dashboard"],
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
            sql = "select obi.CRM_DWH_PKG.FUN_GET_DATA('TRANG_CHU') FROM DUAL"
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
        description="Module = [tong_so_but_toan, tang_truong_huy_dong, thu_phi_dich_vu ]",
        request=ChartRequestSerializer,
        responses={
            status.HTTP_201_CREATED: ChartResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart(self, request):
        try:
            serializer = ChartRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            module = serializer.validated_data['module']
            # module = 'BUT_TOAN'

            con, cur = lib.connect()

            # call the function
            sql = "select obi.CRM_DWH_PKG.FUN_GET_CHART(P_MAN_HINH=>'{P_MAN_HINH}',P_MODULE=>'{P_MODULE}') FROM DUAL".format(P_MAN_HINH="TRANG_CHU,", P_MODULE=module)
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
                        'title': data[6].strip(),
                        'val': data[2],
                        'unit': data[7].strip()
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

