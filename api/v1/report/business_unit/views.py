import cx_Oracle
import api.v1.function as lib

from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.business_unit.serializers import ChartFRequestSerializer, ChartFResponseSerializer, DataResponseSerializer

class BusinessUnitView(BaseAPIView):
    @extend_schema(
        operation_id='Data',
        summary='List',
        tags=["BUSINESS_UNIT"],
        description="Data",
        responses={
            status.HTTP_201_CREATED: DataResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def data(self, request):
        try:
            con, cur = lib.connect()

            sql = "select obi.CRM_DWH_PKG.FUN_GET_DATA('C_02_01') FROM DUAL"
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
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Chart',
        summary='List',
        tags=["BUSINESS_UNIT"],
        description=(
            """
            `name` has values: `tong_thu_nhap_thuan`, `tong_chi_phi_hoat_dong`, `tong_so_don_vi`, `quan_ly_khach_hang`. 
            `unit`=`all` filter only region
            """
        ),
        request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: ChartFResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart(self, request):
        try:
            serializer = ChartFRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            name = serializer.validated_data['name']
            region = serializer.validated_data['region']
            unit = serializer.validated_data['unit']

            con, cur = lib.connect()
            if unit == "all":
                sql = "select obi.CRM_DWH_PKG.FUN_GET_CHART(P_MAN_HINH=>'C_02_01',P_MODULE=>'{P_MODULE}',P_VUNG=>'{P_VUNG}') FROM DUAL".format(P_MODULE=name, P_VUNG=region)
            else:
                sql = "select obi.CRM_DWH_PKG.FUN_GET_CHART(P_MAN_HINH=>'C_02_01',P_MODULE=>'{P_MODULE}',P_DV=>'{P_DV}') FROM DUAL".format(
                    P_MODULE=name, P_DV=unit)

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
                        'key': lib.create_key(data[1].strip()),
                        'label': data[1].strip(),
                        'val': data[2],
                        'unit': data[3].strip()
                    }
                    datas.append(val)

                # datas.sort(key=myBranch)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)