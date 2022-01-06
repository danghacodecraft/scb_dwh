import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.all.serializers import ChartResponseSerializer, PFSChartResponseSerializer, EnterpriseChartResponseSerializer

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

            vung = ""
            kv = ""
            if 'vung' in params.keys() and params['vung'] != 'ALL':
                vung = ",P_VUNG=>'{}'".format(params['vung'])
            elif 'kv' in params.keys() and params['kv'] != 'ALL':
                kv = ",P_VUNG=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                if params['dv'] != 'ALL':
                    dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH =>'{}'{}{}{}{}{}) FROM DUAL".format(screen, key,
                                                                                                       division, kv,
                                                                                                       vung, dv)
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
                        'CHITIEU': data[1].replace("  ", " "),
                        'SODU_DS_LK_KYT': data[2],
                        'THUC_HIEN_KY_T': data[3],
                        'KE_HOACH_KY_T': data[4],
                        'TYLE_KY_T': data[5],
                        'THUC_HIEN_LK': data[6],
                        'KE_HOACH_LK': data[7],
                        'TY_LY_LK': data[8],
                        'DIEM_CHI_TIEU_LK': lib.parseFloat(data[9]),
                        'DIEM_KH_LK': lib.parseFloat(data[10]),
                        'KH_NAM': data[11],
                        'TY_LE_NAM': data[12],
                        'DIEM_CHI_TIEU_KH_NAM': lib.parseFloat(data[13]),
                        'DIEM_KH_NAM': lib.parseFloat(data[14]),
                        'AMOUNT_CHART': lib.parseFloat(data[15])
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
            vung = ""
            if 'kv' in params.keys():
                kv = ",P_VUNG=>'{}'".format(params['kv'])
            elif 'vung' in params.keys():
                vung = ",P_VUNG=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH=>'{}'{}{}{}) FROM DUAL".format(screen, kv, vung, dv)
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
                        'REGION_ID': data[0].strip(),
                        'REGION_NAME': data[1].strip(),
                        'TY_LE_HTKH_LUY_KE_TANG_TRUONG_HDBQ_CKH': data[2].strip(),
                        'DIEM_HTKH_LUY_KE_TANG_TRUONG_HDBQ_CKH': lib.parseFloat(data[3]),
                        'TY_LE_HTKH_LUY_KE_TANG_TRUONG_HDBQ_KKH': data[4].strip(),
                        'DIEM_HTKH_LUY_KE_TANG_TRUONG_HDBQ_KKH': lib.parseFloat(data[5]),
                        'TY_LE_HTKH_DSGN': data[6].strip(),
                        'DIEM_HTKH_DSGN': lib.parseFloat(data[7]),
                        'TY_LE_HTKH_TPDV': data[8].strip(),
                        'DIEM_HTKH_TPDV': lib.parseFloat(data[9]),
                        'TY_LE_LNTT': data[10].strip(),
                        'DIEM_LNTT': lib.parseFloat(data[11]),
                        'TY_LE_BHNT': data[12].strip(),
                        'DIEM_BHNT': lib.parseFloat(data[13]),
                        'TY_LE_TDQT_MOI': data[14].strip(),
                        'DIEM_TDQT_MOI': lib.parseFloat(data[15]),
                        'TY_LE_TPBQ': data[16].strip(),
                        'DIEM_TPBQ': lib.parseFloat(data[17]),
                        'TY_LE_PHAT_TRIEN_KH_MOI': data[18].strip(),
                        'DIEM_PHAT_TRIEN_KH_MOI': lib.parseFloat(data[19]),
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
            vung = ""
            if 'kv' in params.keys() and params['kv'] != 'ALL':
                kv = ",P_VUNG=>'{}'".format(params['kv'])
            elif 'vung' in params.keys() and params['vung'] != 'ALL':
                vung = ",P_VUNG=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH=>'{}'{}{}{}) FROM DUAL".format(screen, kv, vung, dv)
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
                        'STT': data[0],
                        'MONTH_ID': data[1],
                        'BRANCH_ID': data[2],
                        'BRANCH_NAME': data[3],
                        'SORT_REGION': data[4],
                        'HE_SO_DIEM_THEO_MO_HINH_DVKD': data[5],
                        'HTKH_LK_TANG_TRUONG_HD': data[6].strip(),
                        'DIEM_TANG_TRUONG_HD': lib.parseFloat(data[7]),
                        'DIEM_TANG_TRUONG_HDVON_BQ_KKH': lib.parseFloat(data[8]),
                        'HTKH_LK_TANG_TRUONG_CHOVAY': lib.parseFloat(data[9]),
                        'DIEM_TANG_TRUONG_CHOVAY': lib.parseFloat(data[10]),
                        'HTKH_LK_TANG_TRUONG_CHOVAY_BQ': lib.parseFloat(data[11]),
                        'DIEM_TANG_TRUONG_CHOVAY_BQ': lib.parseFloat(data[12]),
                        'HTKH_LK_THU_PHI_DICH_VU': lib.parseFloat(data[13]),
                        'DIEM_THU_PHI_DICH_VU': lib.parseFloat(data[14]),
                        'HTKH_LK_THUPHI_TTQT_LNKDNH': lib.parseFloat(data[15]),
                        'DIEM_THUPHI_TTQT_LNKDNH': lib.parseFloat(data[16]),
                        'HTKH_LK_DOANHSO_THANHTOAN_QR': lib.parseFloat(data[17]),
                        'DIEM_DOANHSO_THANHTOAN_QR': lib.parseFloat(data[18]),
                        'HTKH_LK_MERCHANT_QR': lib.parseFloat(data[19]),
                        'DIEM_MERCHANT_QR': lib.parseFloat(data[20]),
                        'HTKH_LK_DOANHSO_THANHTOAN_POS': lib.parseFloat(data[21]),
                        'DIEM_DOANHSO_THANHTOAN_POS': lib.parseFloat(data[22]),
                        'HTKH_LK_LOI_NHUAN_TRUOC_THUE': lib.parseFloat(data[23]),
                        'DIEM_LOI_NHUAN_TRUOC_THUE': lib.parseFloat(data[24]),
                        'HTKH_LK_SLKH_MOI': lib.parseFloat(data[25]),
                        'DIEM_SLKH_MOI': lib.parseFloat(data[26]),
                        'HTKH_LK_SLHD_EBANKING': lib.parseFloat(data[27]),
                        'DIEM_SLHD_EBANKING': lib.parseFloat(data[28]),
                        'HTKH_LK_KHMOI_SPVAYTIEN': lib.parseFloat(data[29]),
                        'DIEM_KHMOI_SPVAYTIEN': lib.parseFloat(data[30]),
                        'HTKH_LK_DOANHSO_BAOLANH': lib.parseFloat(data[31]),
                        'DIEM_DOANHSO_BAOLANH': lib.parseFloat(data[32]),
                        'DIEM_CHITIEU_CHATLUONG_DICHVU': lib.parseFloat(data[33]),
                        'DIEM_CHITIEU_QLRR': lib.parseFloat(data[34]),
                        'DIEM_CBNV_NGHI_VIEC': lib.parseFloat(data[35]),
                        'DIEM_TYLE_NO2_PHATSINH': lib.parseFloat(data[36]),
                        'DIEM_TYLE_NOXAU_PHATSINH': lib.parseFloat(data[37]),
                        'HTKH_LK_XULY_NOXAU_THONGTHUONG': lib.parseFloat(data[38]),
                        'DIEM_XULY_NOXAU_THONGTHUONG': lib.parseFloat(data[39]),
                        'DIEM_KHUYEN_KHICH': lib.parseFloat(data[40]),
                        'TONG_DIEM': lib.parseFloat(data[41]),
                        'DIEU_CHINHG_TONG_DIEM': lib.parseFloat(data[42]),
                        'TONG_DIEM_SAU_DIEU_CHINH': lib.parseFloat(data[43]),
                        'XEP_HANG': lib.parseFloat(data[44]),
                        'XEP_LOAI': lib.parseFloat(data[45]),
                        'STATUS': data[46],
                        'PROCESS_DATE': data[47],
                        # 'Tang_truong_huy_dong_von_binh_quan_kkh_ty_le_htkh_luy_ke': data[8].strip(),
                        # 'Tang_truong_huy_dong_von_binh_quan_kkh_diem': data[9],
                        # 'Tang_truong_cho_vay_ty_le_htkh_luy_ke': data[10].strip(),
                        # 'Tang_truong_cho_vay_diem': data[11],
                        # 'Tang_truong_cho_vay_binh_quan_ty_le_ktkh_luy_ke': data[12].strip(),
                        # 'Tang_truong_cho_vay_binh_quan_diem': data[13],
                        # 'Thu_phi_dich_vu_ty_le_ktkh_luy_ke': data[14].strip(),
                        # 'Thu_phi_dich_vu_diem': data[15],
                        # 'Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke': data[16].strip(),
                        # 'Thu_phi_dich_vu_bao_gom_thu_phu_ttqt_va_ln_kdnh_diem': data[17],
                        # 'Thu_phi_ttqt_va_ln_kdnh_ty_le_htkh_luy_ke': data[18].strip(),
                        # 'Thu_phi_ttqt_va_ln_kdnh_diem': data[19],
                        # 'Doanh_so_thanh_toan_qr_ty_le_htkh_luy_ke': data[20].strip(),
                        # 'Doanh_so_thanh_toan_qr_diem': data[21],
                        # 'Doanh_so_thanh_toan_pos_ty_le_htkh_luy_ke': data[22].strip(),
                        # 'Doanh_so_thanh_toan_pos_diem': data[23],
                        # 'Loi_nhuan_truoc_thue_ty_le_ktkh_luy_ke': data[24].strip(),
                        # 'Loi_nhuan_truoc_thue_diem': data[25],
                        # 'So_luong_khach_hang_moi_ty_le_htkh_luy_ke': data[26].strip(),
                        # 'So_luong_khach_hang_moi_diem': data[27],
                        # 'So_luong_hop_dong_ebanking_ty_le_htkh_luy_ke': data[28].strip(),
                        # 'So_luong_hop_dong_ebanking_diem': data[29],
                        # 'So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_ty_le_ktkh_luy_ke': data[30].strip(),
                        # 'So_luong_khach_hang_moi_co_su_dung_san_pham_tien_vay_diem': data[31],
                        # 'Doanh_so_bao_lanh_ty_le_htkh_luy_ke': data[32].strip(),
                        # 'Doanh_so_bao_lanh_diem': data[33],
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