import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.enterprise.serializers import HRResponseSerializer, KPIResponseSerializer, IncomeResponseSerializer, BusinessResponseSerializer

class EnterpriseView(BaseAPIView):
    @extend_schema(
        operation_id='Chart HR',
        summary='List',
        tags=["ENTERPRISE"],
        description="""
Screen `C_04`
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: HRResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_hr(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()
            screen = "C_04"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            kv = ""
            if 'kv' in params.keys():
                kv = ",P_KV=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C04_CHART( P_MAN_HINH=>'{}',P_MODULE=>'dinh_bien_nhan_su'{}{} ) FROM DUAL".format(screen, kv, dv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    data_cursor = None

                for data in data_cursor:
                    val = {
                        'AREA_NAME': lib.parseString(data[0]),
                        'SLNS_DINH_BIEN': lib.parseFloat(data[1]),
                        'SLNS_KY_NAY': lib.parseFloat(data[2]),
                        'SLNS_KY_TRUOC': lib.parseFloat(data[3])
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

    @extend_schema(
        operation_id='Chart KPI',
        summary='List',
        tags=["ENTERPRISE"],
        description="""
Screen `ALL`, kv = `ALL`, dv = `001`, ccy = `VND`
- **kpi_chi_tiet_nhanvien**

Screen `C_04`
- **kpi_chart_khu_vuc**.
- **kpi_cac_don_vi_kinh_doanh**.
- **kpi_chi_tiet_nhanvien**

""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="key", type=OpenApiTypes.STR, description="key"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
            OpenApiParameter(
                name="ccy", type=OpenApiTypes.STR, description="ccy"
            )
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: KPIResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_kpi(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()
            screen = "C_04"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            key = ""
            if 'key' in params.keys():
                key = ", P_MODULE=>'{}'".format(params['key'])

            kv = ""
            if 'kv' in params.keys():
                kv = ", P_KV=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ", P_DV=>'{}'".format(params['dv'])

            ccy = ""
            if 'ccy' in params.keys():
                ccy = ", P_CCY=>'{}'".format(params['ccy'])

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C04_CHART( P_MAN_HINH=>'{}'{}{}{}{} ) FROM DUAL".format(screen, key, kv, dv, ccy)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    data_cursor = None

                for data in data_cursor:
                    if key == ", P_MODULE=>'kpi_chart_khu_vuc'":
                        val = {
                            'branch_name': lib.parseString(data[0]),
                            'SLNS_DANH_GIA': lib.parseFloat(data[1]),
                            'SLNS_HOAN_THANH': lib.parseFloat(data[2]),
                            'TY_LE_HOAN_THANH': lib.parseString(data[3]),
                            'TIME': lib.parseString(data[4])
                        }
                    else:
                        val = {
                            'branch_name': lib.parseString(data[0]),
                            'REGION_NAME': lib.parseString(data[1]),
                            'SLNS_DANH_GIA': lib.parseFloat(data[2]),
                            'TY_LE_HOAN_THANH': lib.parseString(data[3]),
                            'KET_QUA_HOAN_THANH': lib.parseFloat(data[4]),
                            'KY_DANH_GIA': lib.parseString(data[5])
                        }

                        if len(data) > 5:
                            val['KY_DANH_GIA'] = data[5]

                    datas.append(val)

                # datas.sort(key=myBranch)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Chart Income',
        summary='List',
        tags=["ENTERPRISE"],
        description="""
Screen `C_04` 
- **thu_nhap_vay_gui**.
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="key", type=OpenApiTypes.STR, description="key"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: IncomeResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_income(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()

            key = params['key']
            screen = "C_04"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            kv = ""
            if 'kv' in params.keys():
                kv = ",P_KV=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C04_CHART( P_MAN_HINH=>'{}',P_MODULE=>'{}'{}{} ) FROM DUAL".format(screen, key, kv, dv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    data_cursor = None

                for data in data_cursor:
                    val = {
                        'BR': lib.parseString(data[0]),
                        'TIEU_DE': lib.parseString(data[1]),
                        'AMT': lib.parseFloat(data[2]),
                        'UNIT': lib.parseString(data[3]),
                        'NIM_HUY_DONG': lib.parseFloat(data[4]) if len(data) > 4 else 0,
                        'NIM_CHO_VAY': lib.parseFloat(data[5]) if len(data) > 5 else 0
                    }
                    # if len(data) > 4:
                    #     val['NIM_HUY_DONG'] = data[4]
                    # if len(data) > 5:
                    #     val['NIM_CHO_VAY'] = data[5]

                    datas.append(val)
                # datas.sort(key=myBranch)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Chart Business',
        summary='List',
        tags=["ENTERPRISE"],
        description="""
Screen `C_04`
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: BusinessResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_business(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()
            screen = "C_04"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            kv = ""
            if 'kv' in params.keys():
                kv = ",P_KV=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C04_CHART( P_MAN_HINH=>'{}',P_MODULE=>'chi_tieu_kinh_doanh'{}{} ) FROM DUAL".format(screen, kv, dv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    data_cursor = None

                for data in data_cursor:
                    val = {
                        'NAME': lib.parseString(data[0]),
                        'THANG': lib.parseFloat(data[1]),
                        'LUY_KE': lib.parseFloat(data[2]),
                        'NAM': lib.parseFloat(data[3]),
                        'ID_NAME': lib.parseString(data[4])
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

