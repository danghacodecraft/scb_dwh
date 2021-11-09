import cx_Oracle
import config.database as db
import json
from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.dashboard.serializers import DashboardResponseSerializer, DashboardChartRequestSerializer, DashboardChartResponseSerializer

class DashboardView(BaseAPIView):
    @extend_schema(
        operation_id='get-data',
        summary='List',
        tags=["Dashboard"],
        description='Get Data',
        responses={
            status.HTTP_201_CREATED: DashboardResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def data(self, request):
        try:
            # create a connection to the Oracle Database
            con = cx_Oracle.connect(db.DATABASE['USER'], db.DATABASE['PASSWORD'], db.DATABASE['NAME'])
            # create a new cursor
            cur = con.cursor()

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

                    print(data_cursor)
                except:
                    print("Loi data ")
                    data_cursor = None

                for data in data_cursor:
                    print(data)
                    val = {
                        'id': data[0],
                        "title": data[6],
                        'day': data[2],
                        'week': data[3],
                        'month': data[4],
                        'accumulated': data[5]
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
        operation_id='get-chart',
        summary='List',
        tags=["Dashboard"],
        description="Module = [I, III, BUT_TOAN]",
        request=DashboardChartRequestSerializer,
        responses={
            status.HTTP_201_CREATED: DashboardChartResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart(self, request):
        try:
            serializer = DashboardChartRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            module = serializer.validated_data['module']
            # module = 'BUT_TOAN'

            # create a connection to the Oracle Database
            con = cx_Oracle.connect(db.DATABASE['USER'], db.DATABASE['PASSWORD'], db.DATABASE['NAME'])
            # create a new cursor
            cur = con.cursor()
            # call the function
            sql = "select obi.CRM_DWH_PKG.FUN_GET_CHART(P_MAN_HINH=>'{P_MAN_HINH}',P_MODULE=>'{P_MODULE}') FROM DUAL".format(P_MAN_HINH="TRANG_CHU,", P_MODULE=module)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                try:
                    data_cursor = res[0]

                    print(data_cursor)
                except:
                    print("Loi data ")
                    data_cursor = None

                for data in data_cursor:
                    print(data)
                    val = {
                        'id': data[0],
                        'title': data[6],
                        'val': data[2],
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