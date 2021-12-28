import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.all.serializers import ChartResponseSerializer, PFSChartResponseSerializer, EnterpriseChartResponseSerializer

def parseFloat(data):
    if data is None:
        return 0
    return float(data.strip())

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


    @extend_schema(
        operation_id='Chart_PFS',
        summary='List',
        tags=["ALL"],
        description="""
Screen `C_06_02_02_02`
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
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
            status.HTTP_201_CREATED: PFSChartResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_pfs(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()
            screen = "C_06_02_02_02"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            kv = ""
            if 'kv' in params.keys():
                kv = ",P_KV=>'{}'".format(params['kv'])

            vung = ""
            if 'vung' in params.keys():
                vung = ",P_VUNG=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "select obi.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH=>'{}'{}{}{}) FROM DUAL".format(screen, kv, vung, dv)
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
                        'Tang_truong_huy_dong_binh_quan_ckh_ty_le_htkh_luy_ke': data[0].strip(),
                        'Tang_truong_huy_dong_binh_quan_ckh_diem': data[1].strip(),
                        'Tang_truong_huy_dong_binh_quan_kkh_ty_le_htkh_luy_ke': data[2].strip(),
                        'Tang_truong_huy_dong_binh_quan_kkh_diem': parseFloat(data[3]),
                        'Doanh_so_giai_ngan_ty_le_htkh_luy_ke': data[4].strip(),
                        'Doanh_so_giai_ngan_diem': parseFloat(data[5]),
                        'Thu_phi_dich_vu_ty_le_htkh_luy_ke': data[6].strip(),
                        'Thu_phu_dich_vu_diem': parseFloat(data[7]),
                        'Loi_nhuan_truoc_thue_ty_le_htkh_luy_ke': data[8].strip(),
                        'Loi_nhuan_truoc_thue_diem': parseFloat(data[9]),
                        'Doanh_so_bao_hiem_nhan_tho_ty_le_htkh_luy_ke': data[10].strip(),
                        'Doanh_so_bao_hiem_nhan_tho_diem': parseFloat(data[11]),
                        'So_luong_the_tdqt_phat_hanh_moi_ty_le_htkh_luy_ke': data[12].strip(),
                        'So_luong_the_tdqt_phat_hanh_moi_diem': parseFloat(data[13]),
                        'So_du_trai_phieu_binh_quan_ty_le_htkh_luy_ke': data[14].strip(),
                        'So_du_trai_phieu_binh_quan_diem': parseFloat(data[15]),
                        'Phat_trien_khach_hang_moi_ty_le_htkh_luy_ke': data[16].strip(),
                        'Phat_trien_khach_hang_moi_diem': parseFloat(data[17]),
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
        operation_id='Chart_Enterprise',
        summary='List',
        tags=["ALL"],
        description="""
Screen `C_06_03_02_03`
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
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
            status.HTTP_201_CREATED: EnterpriseChartResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_enterprise(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()
            screen = "C_06_03_02_03"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            kv = ""
            if 'kv' in params.keys():
                kv = ",P_KV=>'{}'".format(params['kv'])

            vung = ""
            if 'vung' in params.keys():
                vung = ",P_VUNG=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "select obi.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH=>'{}'{}{}{}) FROM DUAL".format(screen, kv, vung, dv)
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

                # for data in data_cursor:
                #     print(data)
                #     print("=================={}".format(len(data)))
                #     val = {
                #         'Tang_truong_huy_dong_ty_le_htkh_luy_ke': data[6].strip(),
                #         'Tang_truong_huy_dong_ty_le_htkh_diem': data[7],
                #         'Tang_truong_huy_dong_von_binh_quan_kkh_ty_le_htkh_luy_ke': data[8].strip(),
                #         'Tang_truong_huy_dong_von_binh_quan_kkh_diem': data[9],
                #         'Tang_truong_cho_vay_ty_le_htkh_luy_ke': data[10].strip(),
                #         'Tang_truong_cho_vay_diem': data[11],
                #         'Tang_truong_cho_vay_binh_quan_ty_le_ktkh_luy_ke': data[12].strip(),
                #         'Tang_truong_cho_vay_binh_quan_diem': data[13],
                #         'Thu_phi_dich_vu_ty_le_ktkh_luy_ke': data[14].strip(),
                #         'Thu_phi_dich_vu_diem': data[15],
                #         'Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke': data[16].strip(),
                #         'Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_diem': data[17],
                #         'Thu_phi_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke': data[18].strip(),
                #         'Thu_phi_ttqt_va_ln_kdnh_diem': data[19],
                #         'Doanh_so_thanh_toan_qr_ty_le_htkh_luy_ke': data[20].strip(),
                #         'Doanh_so_thanh_toan_qr_diem': data[21],
                #         'Doanh_so_thanh_toan_pos_ty_le_htkh_luy_ke': data[22].strip(),
                #         'Doanh_so_thanh_toan_pos_diem': data[23],
                #         'Loi_nhuan_truoc_thue_ty_le_ktkh_luy_ke': data[24].strip(),
                #         'Loi_nhuan_truoc_thue_diem': data[25],
                #         'So_luong_khach_hang_moi_ty_le_htkh_luy_ke': data[26].strip(),
                #         'So_luong_khach_hang_moi_diem': data[27],
                #         'So_luong_hop_dong_ebanking_ty_le_htkh_luy_ke': data[28].strip(),
                #         'So_luong_hop_dong_ebanking_diem': data[29],
                #         'So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_ty_le_ktkh_luy_ke': data[30].strip(),
                #         'So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_diem': data[31],
                #         'Doanh_so_bao_lanh_ty_le_htkh_luy_ke': data[32].strip(),
                #         'Doanh_so_bao_lanh_diem': data[33],
                #     }
                #     datas.append(val)
                # datas.sort(key=myBranch)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)