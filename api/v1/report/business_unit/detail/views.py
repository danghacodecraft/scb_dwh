import cx_Oracle
import api.v1.function as lib

from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.business_unit.detail.serializers import ChartDetailRequestSerializer, ChartFResponseSerializer, DataResponseSerializer

class BusinessDetailUnitView(BaseAPIView):
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

            sql = "select obi.CRM_DWH_PKG.FUN_GET_DATA('C_02_02') FROM DUAL"
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
            The `name` has values: 
                `quan_ly_khach_hang_bde`, 
                `thu_nhap_thuan_tu_dich_vu_the_gn_visa`, 
                `bao_cao_cif_mo_moi`, 
                `thu_nhap_thuan_tu_dich_vu_the_pos`, 
                `tong_chi_phi_hoat_dong_hoat_dong`, 
                `tong_chi_phi_hoat_dong_nhan_vien`, 
                `tong_chi_phi_hoat_dong_dau_tu`, 
                `cho_vay_khach_hang`, 
                `thu_nhap_thuan_tu_dich_vu_the_tdqt`, 
                `quan_ly_khach_hang_g`, 
                `quan_ly_khach_hang_m`, 
                `thu_nhap_thuan_tu_dvkh`, 
                `tong_thu_nhap_thuan`, 
                `thu_nhap_thuan_tu_dich_vu_the_td_mc`, 
                `tong_chi_phi_hoat_dong_thue`, 
                `quan_ly_khach_hang_pp+`, 
                `quan_ly_khach_hang_r`, 
                `quan_ly_khach_hang_sli`, 
                `quan_ly_khach_hang`, 
                `quan_ly_khach_hang_bd`, 
                `quan_ly_khach_hang_bdi`, 
                `quan_ly_khach_hang_n`, 
                `thu_nhap_thuan_tu_dich_vu_the_atm`, 
                `quan_ly_khach_hang_sap`, 
                `quan_ly_khach_hang_di`, 
                `quan_ly_khach_hang_pp`, 
                `quan_ly_khach_hang_ti`, 
                `huy_dong_von`, 
                `thu_nhap_thuan_tu_dich_vu_the_may_atm`, 
                `quan_ly_khach_hang_d`, 
                `thu_nhap_thuan_tu_dich_vu_the`, 
                `tong_chi_phi_hoat_dong`, 
                `tong_so_don_vi`, 
                `thu_nhap_thuan_tu_dich_vu_the_gn_mc`, 
                `tong_chi_phi_hoat_dong_tai_san`, 
                `quan_ly_khach_hang_de`, 
                `quan_ly_khach_hang_p`
            """
        ),
        request=ChartDetailRequestSerializer,
        responses={
            status.HTTP_201_CREATED: ChartFResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart(self, request):
        try:
            serializer = ChartDetailRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            name = serializer.validated_data['name']

            con, cur = lib.connect()
            sql = "select obi.CRM_DWH_PKG.FUN_GET_CHART(P_MAN_HINH=>'C_02_02',P_MODULE=>'{P_MODULE}') FROM DUAL".format(
                    P_MODULE=name)

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

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)