import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.all.serializers import ChartResponseSerializer

class AllView(BaseAPIView):
    @extend_schema(
        operation_id='Chart',
        summary='List',
        tags=["ALL"],
        description="""
Screen `C_06`
- **ket_qua_chi_tieu_ke_hoach**.

`division`
- **TH0**: TOÀN HÀNG 
- **A**: KHỐI DVNH&TCCN
- **B**: KHỐI DOANH NGHIỆP
- **C**: KHỐI KDTT
- **H**: KHỐI XLN&KTTS

""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="key", type=OpenApiTypes.STR, description="key"
            ),
            OpenApiParameter(
                name="division", type=OpenApiTypes.STR, description="division"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
        ],
        # request=ChartFRequestSerializer,
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
            screen = "C_06"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            key = ",P_MODULE=>'ket_qua_chi_tieu_ke_hoach'"
            if 'key' in params.keys():
                key = ",P_MODULE=>'{}'".format(params['key'])

            division = ""
            if 'division' in params.keys():
                division = ",P_DIVISION=>'{}'".format(params['division'])

            kv = ""
            if 'kv' in params.keys():
                kv = ",P_KV=>'{}'".format(params['kv'])

            vung = ""
            if 'vung' in params.keys():
                vung = ",P_VUNG=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "select  obi.crm_dwh_pkg.FUN_C06_CHART(P_MAN_HINH =>'{}'{}{}{}{}{}) from dual".format(screen, key, division, kv, vung, dv)
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
                        'PROCESS_DATE': data[0],
                        'CHITIEU': data[1],
                        'SODU_DS_LK_KYT': data[2],
                        'THUC_HIEN_KY_T': data[3],
                        'KE_HOACH_KY_T': data[4],
                        'TYLE_KY_T': data[5],
                        'THUC_HIEN_LK': data[6],
                        'KE_HOACH_LK': data[7],
                        'TY_LY_LK': data[8],
                        'DIEM_CHI_TIEU_LK': data[9],
                        'DIEM_KH_LK': data[10],
                        'KH_NAM': data[11],
                        'TY_LE_NAM': data[12],
                        'DIEM_CHI_TIEU_KH_NAM': data[13],
                        'DIEM_KH_NAM': data[14],
                        'AMOUNT_CHART': data[15]
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
