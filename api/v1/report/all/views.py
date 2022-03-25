import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.all.serializers import ChartResponseSerializer, PFSChartResponseSerializer, EnterpriseChartResponseSerializer, ChartBonusResponseSerializer

# Tăng trưởng Huy động CKH.
# Tăng trưởng Huy động KKH.
# Tăng trưởng Cho vay.
# Thu nhập thuần từ dịch vụ.
# Lợi nhuận trước thuế.
# Chỉ tiêu giám sát.
# Lợi nhuận từ hoạt động cấp Tín dụng/Tài sản tính theo rủi ro tín dụng.
# Tỷ lệ nợ nhóm 2 phát sinh trong năm.
# Tỷ lệ nợ xấu phát sính trong năm.
# Chỉ tiêu khác.
# Số lượng khách hàng hoạt động phát triển mới.
# TOI phí dịch vụ/ 01 khách hàng CN.
# TOI phí dịch vụ khách hàng cá nhân.
# Số lượng khách hàng cá nhân bình quân.
# Tỷ lệ nợ nhóm 2.
# Tỷ lệ nợ xấu.
# KHỐI DVNH&TCCN.
# Chỉ tiêu tài chính.
# Doanh số bảo hiểm nhân thọ.
# Số lượng thẻ TDQT phát hành mới.
# Số dư trái phiếu bình quân.
# Phát triển khách hàng mới.
# Chỉ tiêu Chất lượng dịch vụ.
# Chỉ tiêu Quản lý rủi ro (Xếp hạng tuân thủ).
# Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ CBNV nghỉ việc).
# Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ hoàn thành tháp đào tạo).
# Tỷ lệ nợ xấu phát sinh trong năm.
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

            key = "" #,P_MODULE=>'ket_qua_chi_tieu_ke_hoach'"
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

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH=>'{}'{}{}{}{}{}) FROM DUAL".format(screen, key, division, kv, vung, dv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            lstsum = [
                "Doanh số bảo hiểm nhân thọ",
                "Số lượng thẻ TDQT phát hành mới",
                "Số dư trái phiếu bình quân",
                "Phát triển khách hàng mới"
            ]
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    print("Loi data ")
                    data_cursor = None

                dicdatas = {}

                for data in data_cursor:
                    chitieu = lib.parseString(data[1])
                    branchid = lib.parseString(data[16])
                    val = {
                        'PROCESS_DATE': lib.parseString(data[0]),
                        'CHITIEU': chitieu,

                        'SODU_DS_LK_KYT': lib.parseFloat(data[2]),
                        'THUC_HIEN_KY_T': lib.parseFloat(data[3]),
                        'KE_HOACH_KY_T': lib.parseFloat(data[4]),
                        'TYLE_KY_T': lib.parseFloat(data[5]),
                        'THUC_HIEN_LK': lib.parseFloat(data[6]),
                        'KE_HOACH_LK': lib.parseFloat(data[7]),
                        'TY_LY_LK': lib.parseFloat(data[8]),
                        'DIEM_CHI_TIEU_LK': lib.parseFloat(data[9]),
                        'DIEM_KH_LK': lib.parseFloat(data[10]),
                        'KH_NAM': lib.parseFloat(data[11]),
                        'TY_LE_NAM': lib.parseFloat(data[12]),
                        'DIEM_CHI_TIEU_KH_NAM': lib.parseFloat(data[13]),
                        'DIEM_KH_NAM': lib.parseFloat(data[14]),
                        'AMOUNT_CHART': lib.parseFloat(data[15]),
                        'BRANCH_ID': branchid
                    }

                    if chitieu not in lstsum:
                        datas.append(val)
                        continue

                    if branchid not in dicdatas:
                        dicdatas[branchid] = val
                    else:
                        d = dicdatas[branchid]
                        d['SODU_DS_LK_KYT'] = d['SODU_DS_LK_KYT'] + lib.parseFloat(data[2], 2, False)
                        d['THUC_HIEN_KY_T'] = d['THUC_HIEN_KY_T'] + lib.parseFloat(data[3], 2, False)
                        d['KE_HOACH_KY_T'] = d['KE_HOACH_KY_T'] + lib.parseFloat(data[4], 2, False)
                        d['TYLE_KY_T'] = d['TYLE_KY_T'] + lib.parseFloat(data[5], 2, False)
                        d['THUC_HIEN_LK'] = d['THUC_HIEN_LK'] + lib.parseFloat(data[6], 2, False)
                        d['KE_HOACH_LK'] = d['KE_HOACH_LK'] + lib.parseFloat(data[7], 2, False)
                        d['TY_LY_LK'] = d['TY_LY_LK'] + lib.parseFloat(data[8], 2, False)
                        d['DIEM_CHI_TIEU_LK'] = d['DIEM_CHI_TIEU_LK'] + lib.parseFloat(data[9], 2, False)
                        d['DIEM_KH_LK'] = d['DIEM_KH_LK'] + lib.parseFloat(data[10], 2, False)
                        d['KH_NAM'] = d['KH_NAM'] + lib.parseFloat(data[11], 2, False)
                        d['TY_LE_NAM'] = d['TY_LE_NAM'] + lib.parseFloat(data[12], 2, False)
                        d['DIEM_CHI_TIEU_KH_NAM'] = d['DIEM_CHI_TIEU_KH_NAM'] + lib.parseFloat(data[13], 2, False)
                        d['DIEM_KH_NAM'] = d['DIEM_KH_NAM'] + lib.parseFloat(data[14], 2, False)
                        d['AMOUNT_CHART'] = d['AMOUNT_CHART'] + lib.parseFloat(data[15], 2, False)

                for k in dicdatas:
                    dicdatas[k]['SODU_DS_LK_KYT'] = lib.parseFloat(dicdatas[k]['SODU_DS_LK_KYT'], 2, True)
                    dicdatas[k]['THUC_HIEN_KY_T'] = lib.parseFloat(dicdatas[k]['THUC_HIEN_KY_T'], 2, True)
                    dicdatas[k]['KE_HOACH_KY_T'] = lib.parseFloat(dicdatas[k]['KE_HOACH_KY_T'], 2, True)
                    dicdatas[k]['TYLE_KY_T'] = lib.parseFloat(dicdatas[k]['TYLE_KY_T'], 2, True)
                    dicdatas[k]['THUC_HIEN_LK'] = lib.parseFloat(dicdatas[k]['THUC_HIEN_LK'], 2, True)
                    dicdatas[k]['KE_HOACH_LK'] = lib.parseFloat(dicdatas[k]['KE_HOACH_LK'], 2, True)
                    dicdatas[k]['TY_LY_LK'] = lib.parseFloat(dicdatas[k]['TY_LY_LK'], 2, True)
                    dicdatas[k]['DIEM_CHI_TIEU_LK'] = lib.parseFloat(dicdatas[k]['DIEM_CHI_TIEU_LK'], 2, True)
                    dicdatas[k]['DIEM_KH_LK'] = lib.parseFloat(dicdatas[k]['DIEM_KH_LK'], 2, True)
                    dicdatas[k]['KH_NAM'] = lib.parseFloat(dicdatas[k]['KH_NAM'], 2, True)
                    dicdatas[k]['TY_LE_NAM'] = lib.parseFloat(dicdatas[k]['TY_LE_NAM'], 2, True)
                    dicdatas[k]['DIEM_CHI_TIEU_KH_NAM'] = lib.parseFloat(dicdatas[k]['DIEM_CHI_TIEU_KH_NAM'], 2, True)
                    dicdatas[k]['DIEM_KH_NAM'] = lib.parseFloat(dicdatas[k]['DIEM_KH_NAM'], 2, True)
                    dicdatas[k]['AMOUNT_CHART'] = lib.parseFloat(dicdatas[k]['AMOUNT_CHART'], 2, True)
                    datas.append(dicdatas[k])

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
                        'REGION_ID': lib.parseString(data[0]),
                        'REGION_NAME': lib.parseString(data[1]),
                        'TY_LE_HTKH_LUY_KE_TANG_TRUONG_HDBQ_CKH': lib.parseString(data[2]),
                        'DIEM_HTKH_LUY_KE_TANG_TRUONG_HDBQ_CKH': lib.parseFloat(data[3]),
                        'TY_LE_HTKH_LUY_KE_TANG_TRUONG_HDBQ_KKH': lib.parseString(data[4]),
                        'DIEM_HTKH_LUY_KE_TANG_TRUONG_HDBQ_KKH': lib.parseFloat(data[5]),
                        'TY_LE_HTKH_DSGN': lib.parseString(data[6]),
                        'DIEM_HTKH_DSGN': lib.parseFloat(data[7]),
                        'TY_LE_HTKH_TPDV': lib.parseString(data[8]),
                        'DIEM_HTKH_TPDV': lib.parseFloat(data[9]),
                        'TY_LE_LNTT': lib.parseString(data[10]),
                        'DIEM_LNTT': lib.parseFloat(data[11]),
                        'TY_LE_BHNT': lib.parseString(data[12]),
                        'DIEM_BHNT': lib.parseFloat(data[13]),
                        'TY_LE_TDQT_MOI': lib.parseString(data[14]),
                        'DIEM_TDQT_MOI': lib.parseFloat(data[15]),
                        'TY_LE_TPBQ': lib.parseString(data[16]),
                        'DIEM_TPBQ': lib.parseFloat(data[17]),
                        'TY_LE_PHAT_TRIEN_KH_MOI': lib.parseString(data[18]),
                        'DIEM_PHAT_TRIEN_KH_MOI': lib.parseFloat(data[19]),
                        'DIEM_KHUYEN_KHICH': lib.parseFloat(data[20]),
                        'TONG_DIEM': lib.parseFloat(data[21]),
                        'DIEU_CHINH_TONG_DIEM': lib.parseFloat(data[22]),
                        'TONG_DIEM_SAU_DIEU_CHINH': lib.parseFloat(data[23]),
                        'XEP_HANG': lib.parseFloat(data[24]),
                        'XEP_LOAI': lib.parseString(data[25]),
                        'PROCESS_DATE': lib.parseString(data[26])
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
                        'MONTH_ID': lib.parseString(data[1]),
                        'BRANCH_ID': lib.parseString(data[2]),
                        'BRANCH_NAME': lib.parseString(data[3]),
                        'SORT_REGION': lib.parseString(data[4]),
                        'HE_SO_DIEM_THEO_MO_HINH_DVKD': lib.parseString(data[5]),
                        'HTKH_LK_TANG_TRUONG_HD': lib.parseFloat(data[6]),
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

    @extend_schema(
        operation_id='Chart Bonus',
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

            `target`
            -**sale_plan**


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
            OpenApiParameter(
                name="target", type=OpenApiTypes.STR, description="Chỉ Tiêu"
            ),
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: ChartBonusResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_bonus(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()
            screen = "C_06"
            if 'screen' in params.keys():
                screen = format(params['screen'])

            key = "" #,P_MODULE=>'ket_qua_chi_tieu_ke_hoach'"
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

            target = ""
            if 'target' in params.keys():
                target = params['target']

            
            # chitieu = ""
            # if 'chitieu' in params.keys():
            #     chitieu = params['chitieu']


            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH=>'{}'{}{}{}{}{}) FROM DUAL".format(screen, key, division, kv, vung, dv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            loopdata = []

            # Tăng trưởng Huy động CKH
            target_tang_truong_huy_dong_ckh_9 = []
            target_tang_truong_huy_dong_ckh_10 = []
            target_tang_truong_huy_dong_ckh_11 = []
            # Tăng trưởng Huy động KKH
            target_tang_truong_huy_dong_kkh_9 = []
            target_tang_truong_huy_dong_kkh_10 = []
            target_tang_truong_huy_dong_kkh_11 = []
            # Tăng trưởng Cho vay
            target_tang_truong_cho_vay_9 = []
            target_tang_truong_cho_vay_10 = []
            target_tang_truong_cho_vay_11 = []
            # Thu nhập thuần từ dịch vụ
            target_thu_nhap_thuan_tu_dich_vu_9 = []
            target_thu_nhap_thuan_tu_dich_vu_10 = []
            target_thu_nhap_thuan_tu_dich_vu_11 = []
            # Lợi nhuận trước thuế
            target_loi_nhuan_truoc_thue_9 = []
            target_loi_nhuan_truoc_thue_10 = []
            target_loi_nhuan_truoc_thue_11 = []

            # Doanh số bảo hiểm nhân thọ
            target_doanh_so_bao_hiem_nhan_tho_9 = []
            target_doanh_so_bao_hiem_nhan_tho_10 = []
            target_doanh_so_bao_hiem_nhan_tho_11 = []
            # Số lượng thẻ TDQT phát hành mới
            target_so_luong_the_TDQT_phat_hanh_moi_9 = []
            target_so_luong_the_TDQT_phat_hanh_moi_10 = []
            target_so_luong_the_TDQT_phat_hanh_moi_11 = []
            # Số dư trái phiếu bình quân
            target_so_du_trai_phieu_binh_quan_9 = []
            target_so_du_trai_phieu_binh_quan_10 = []
            target_so_du_trai_phieu_binh_quan_11 = []
            # Phát triển khách hàng mới
            target_phat_trien_khach_hang_moi_9 = []
            target_phat_trien_khach_hang_moi_10 = []
            target_phat_trien_khach_hang_moi_11 = []

            # Lợi nhuận từ hoạt động cấp Tín dụng/Tài sản tính theo rủi ro tín dụng
            target_loi_nhuan_tu_hoat_dong_cap_tin_dung_9 = []
            target_loi_nhuan_tu_hoat_dong_cap_tin_dung_10 = []
            target_loi_nhuan_tu_hoat_dong_cap_tin_dung_11 = []
            # Tỷ lệ nợ nhóm 2 phát sinh trong năm
            target_ty_le_no_nhom_2_phat_sinh_trong_nam_9 = []
            target_ty_le_no_nhom_2_phat_sinh_trong_nam_10 = []
            target_ty_le_no_nhom_2_phat_sinh_trong_nam_11 = []
            # Tỷ lệ nợ xấu phát sính trong năm
            # Tỷ lệ nợ xấu phát sinh trong năm
            target_ty_le_no_xau_phat_sinh_trong_nam_9 = []
            target_ty_le_no_xau_phat_sinh_trong_nam_10 = []
            target_ty_le_no_xau_phat_sinh_trong_nam_11 = []

            # Chỉ tiêu Chất lượng dịch vụ
            target_chi_tieu_chat_luong_dich_vu_9 = []
            target_chi_tieu_chat_luong_dich_vu_10 = []
            target_chi_tieu_chat_luong_dich_vu_11 = []
            # Chỉ tiêu Quản lý rủi ro (Xếp hạng tuân thủ)
            target_chi_tieu_quan_ly_rui_ro_9 = []
            target_chi_tieu_quan_ly_rui_ro_10 = []
            target_chi_tieu_quan_ly_rui_ro_11 = []
            # Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ CBNV nghỉ việc)
            target_ty_le_cbnv_nghi_viec_9 = []
            target_ty_le_cbnv_nghi_viec_10 = []
            target_ty_le_cbnv_nghi_viec_11 = []
            # Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ hoàn thành tháp đào tạo)
            target_ty_le_hoan_thanh_thap_dao_tao_9 = []
            target_ty_le_hoan_thanh_thap_dao_tao_10 = []
            target_ty_le_hoan_thanh_thap_dao_tao_11 = []
            
            # Số lượng khách hàng hoạt động phát triển mới
            target_so_luong_kh_moi_9 = []
            target_so_luong_kh_moi_10 = []
            target_so_luong_kh_moi_11 = []
            # TOI phí dịch vụ/ 01 khách hàng CN
            # TOI phí dịch vụ khách hàng cá nhân
            target_toi_phi_dich_vu_khcn_9 = []
            target_toi_phi_dich_vu_khcn_10 = []
            target_toi_phi_dich_vu_khcn_11 = []
            # Số lượng khách hàng cá nhân bình quân
            target_so_luong_khcn_binh_quan_9 = []
            target_so_luong_khcn_binh_quan_10 = []
            target_so_luong_khcn_binh_quan_11 = []
            # Tỷ lệ nợ nhóm 2
            target_ty_le_no_nhom_2_9 = []
            target_ty_le_no_nhom_2_10 = []
            target_ty_le_no_nhom_2_11 = []
            # Tỷ lệ nợ xấu
            target_ty_le_no_xau_9 = []
            target_ty_le_no_xau_10 = []
            target_ty_le_no_xau_11 = []

            target_list = [
                'Tăng trưởng Huy động CKH', 
                'Tăng trưởng Huy động KKH', 
                'Tăng trưởng Cho vay', 
                'Thu nhập thuần từ dịch vụ', 
                'Lợi nhuận trước thuế', 
                'Chỉ tiêu giám sát', 
                'Lợi nhuận từ hoạt động cấp Tín dụng/Tài sản tính theo rủi ro tín dụng', 
                'Tỷ lệ nợ nhóm 2 phát sinh trong năm', 
                'Tỷ lệ nợ xấu phát sính trong năm', 
                'Chỉ tiêu khác', 
                'Số lượng khách hàng hoạt động phát triển mới', 
                'TOI phí dịch vụ/ 01 khách hàng CN', 
                'TOI phí dịch vụ khách hàng cá nhân', 
                'Số lượng khách hàng cá nhân bình quân', 
                'Tỷ lệ nợ nhóm 2', 
                'Tỷ lệ nợ xấu', 
                'KHỐI DVNH&TCCN', 
                'Chỉ tiêu tài chính', 
                'Doanh số bảo hiểm nhân thọ', 
                'Số lượng thẻ TDQT phát hành mới', 
                'Số dư trái phiếu bình quân', 
                'Phát triển khách hàng mới', 
                'Chỉ tiêu Chất lượng dịch vụ', 
                'Chỉ tiêu Quản lý rủi ro (Xếp hạng tuân thủ)', 
                'Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ CBNV nghỉ việc)', 
                'Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ hoàn thành tháp đào tạo)', 
                'Tỷ lệ nợ xấu phát sinh trong năm'
            ]

            # for target_item in target_list:
            #     print(target_item)

            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    print("Loi data ")
                    data_cursor = None

                dicdatas = {}

                for data in data_cursor:
                    process_date = lib.parseString(data[0])
                    chitieu = lib.parseString(data[1])
                    sodu_ds_lk_kyt = lib.parseFloat(data[2])
                    thuc_hien_ky_t = lib.parseFloat(data[3])
                    ke_hoach_ky_t = lib.parseFloat(data[4])
                    tyle_ky_t = lib.parseFloat(data[5])
                    thuc_hien_lk = lib.parseFloat(data[6])
                    ke_hoach_lk = lib.parseFloat(data[7])
                    ty_ly_lk = lib.parseFloat(data[8])
                    diem_chi_tieu_lk = lib.parseFloat(data[9])
                    diem_kh_lk = lib.parseFloat(data[10])
                    kh_nam = lib.parseFloat(data[11])
                    ty_le_nam = lib.parseFloat(data[12])
                    diem_chi_tieu_kh_nam = lib.parseFloat(data[13])
                    diem_kh_nam = lib.parseFloat(data[14])
                    amount_chart = lib.parseFloat(data[15])
                    branchid = lib.parseString(data[16])
                    val = {
                        'PROCESS_DATE':process_date, 
                        'CHITIEU':chitieu, 
                        'SODU_DS_LK_KYT':sodu_ds_lk_kyt, 
                        'THUC_HIEN_KY_T':thuc_hien_ky_t, 
                        'KE_HOACH_KY_T':ke_hoach_ky_t, 
                        'TYLE_KY_T':tyle_ky_t, 
                        'THUC_HIEN_LK':thuc_hien_lk, 
                        'KE_HOACH_LK':ke_hoach_lk, 
                        'TY_LY_LK':ty_ly_lk, 
                        'DIEM_CHI_TIEU_LK':diem_chi_tieu_lk, 
                        'DIEM_KH_LK':diem_kh_lk, 
                        'KH_NAM':kh_nam, 
                        'TY_LE_NAM':ty_le_nam, 
                        'DIEM_CHI_TIEU_KH_NAM':diem_chi_tieu_kh_nam, 
                        'DIEM_KH_NAM':diem_kh_nam, 
                        'AMOUNT_CHART':amount_chart, 
                        'BRANCH_ID': branchid
                    }


                    # if chitieu not in target_list:
                    #     target_list.append(chitieu)


                    if target == 'filter':
                        if branchid.startswith('V') or branchid.startswith('A'):
                            # chỉ tiêu quy mô và hiệu quả
                            if chitieu == 'Tăng trưởng Huy động CKH':
                                if data[0].month == 9:
                                    target_tang_truong_huy_dong_ckh_9.append(data)
                                if data[0].month == 10:
                                    target_tang_truong_huy_dong_ckh_10.append(data)
                                if data[0].month == 11:
                                    target_tang_truong_huy_dong_ckh_11.append(data)
                            if chitieu == 'Tăng trưởng Huy động KKH':
                                if data[0].month == 9:
                                    target_tang_truong_huy_dong_kkh_9.append(data)
                                if data[0].month == 10:
                                    target_tang_truong_huy_dong_kkh_10.append(data)
                                if data[0].month == 11:
                                    target_tang_truong_huy_dong_kkh_11.append(data)
                            if chitieu == 'Tăng trưởng Cho vay':
                                if data[0].month == 9:
                                    target_tang_truong_cho_vay_9.append(data)
                                if data[0].month == 10:
                                    target_tang_truong_cho_vay_10.append(data)
                                if data[0].month == 11:
                                    target_tang_truong_cho_vay_11.append(data)
                            if chitieu == 'Thu nhập thuần từ dịch vụ':
                                if data[0].month == 9:
                                    target_thu_nhap_thuan_tu_dich_vu_9.append(data)
                                if data[0].month == 10:
                                    target_thu_nhap_thuan_tu_dich_vu_10.append(data)
                                if data[0].month == 11:
                                    target_thu_nhap_thuan_tu_dich_vu_11.append(data)
                            if chitieu == 'Lợi nhuận trước thuế':
                                if data[0].month == 9:
                                    target_loi_nhuan_truoc_thue_9.append(data)
                                if data[0].month == 10:
                                    target_loi_nhuan_truoc_thue_10.append(data)
                                if data[0].month == 11:
                                    target_loi_nhuan_truoc_thue_11.append(data)


                            # Chỉ Tiêu Sale Plan
                            if chitieu == 'Doanh số bảo hiểm nhân thọ':
                                if data[0].month == 9:
                                    target_doanh_so_bao_hiem_nhan_tho_9.append(data)
                                if data[0].month == 10:
                                    target_doanh_so_bao_hiem_nhan_tho_10.append(data)
                                if data[0].month == 11:
                                    target_doanh_so_bao_hiem_nhan_tho_11.append(data)
                            if chitieu == 'Số lượng thẻ TDQT phát hành mới':
                                if data[0].month == 9:
                                    target_so_luong_the_TDQT_phat_hanh_moi_9.append(data)
                                if data[0].month == 10:
                                    target_so_luong_the_TDQT_phat_hanh_moi_10.append(data)
                                if data[0].month == 11:
                                    target_so_luong_the_TDQT_phat_hanh_moi_11.append(data)
                            if chitieu == 'Số dư trái phiếu bình quân':
                                if data[0].month == 9:
                                    target_so_du_trai_phieu_binh_quan_9.append(data)
                                if data[0].month == 10:
                                    target_so_du_trai_phieu_binh_quan_10.append(data)
                                if data[0].month == 11:
                                    target_so_du_trai_phieu_binh_quan_11.append(data)
                            if chitieu == 'Phát triển khách hàng mới':
                                if data[0].month == 9:
                                    target_phat_trien_khach_hang_moi_9.append(data)
                                if data[0].month == 10:
                                    target_phat_trien_khach_hang_moi_10.append(data)
                                if data[0].month == 11:
                                    target_phat_trien_khach_hang_moi_11.append(data)

                            # Chỉ tiêu Giám Sát
                            if chitieu == 'Lợi nhuận từ hoạt động cấp Tín dụng/Tài sản tính theo rủi ro tín dụng':
                                if data[0].month == 9:
                                    target_loi_nhuan_tu_hoat_dong_cap_tin_dung_11.append(data)
                                if data[0].month == 10:
                                    target_loi_nhuan_tu_hoat_dong_cap_tin_dung_11.append(data)
                                if data[0].month == 11:
                                    target_loi_nhuan_tu_hoat_dong_cap_tin_dung_11.append(data)
                            if chitieu == 'Tỷ lệ nợ nhóm 2 phát sinh trong năm':
                                if data[0].month == 9:
                                    target_ty_le_no_nhom_2_phat_sinh_trong_nam_9.append(data)
                                if data[0].month == 10:
                                    target_ty_le_no_nhom_2_phat_sinh_trong_nam_10.append(data)
                                if data[0].month == 11:
                                    target_ty_le_no_nhom_2_phat_sinh_trong_nam_11.append(data)
                            if chitieu == 'Tỷ lệ nợ xấu phát sính trong năm' or chitieu == 'Tỷ lệ nợ xấu phát sinh trong năm':
                                if data[0].month == 9:
                                    target_ty_le_no_xau_phat_sinh_trong_nam_9.append(data)
                                if data[0].month == 10:
                                    target_ty_le_no_xau_phat_sinh_trong_nam_10.append(data)
                                if data[0].month == 11:
                                    target_ty_le_no_xau_phat_sinh_trong_nam_11.append(data)
                                
                            # Chỉ tiêu phi tài chính
                            if chitieu == 'Chỉ tiêu Chất lượng dịch vụ':
                                if data[0].month == 9:
                                    target_chi_tieu_chat_luong_dich_vu_9.append(data)
                                if data[0].month == 10:
                                    target_chi_tieu_chat_luong_dich_vu_10.append(data)
                                if data[0].month == 11:
                                    target_chi_tieu_chat_luong_dich_vu_11.append(data)
                            if chitieu == 'Chỉ tiêu Quản lý rủi ro (Xếp hạng tuân thủ)':
                                if data[0].month == 9:
                                    target_chi_tieu_quan_ly_rui_ro_9.append(data)
                                if data[0].month == 10:
                                    target_chi_tieu_quan_ly_rui_ro_10.append(data)
                                if data[0].month == 11:
                                    target_chi_tieu_quan_ly_rui_ro_11.append(data)
                            if chitieu == 'Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ CBNV nghỉ việc)':
                                if data[0].month == 9:
                                    target_ty_le_cbnv_nghi_viec_9.append(data)
                                if data[0].month == 10:
                                    target_ty_le_cbnv_nghi_viec_10.append(data)
                                if data[0].month == 11:
                                    target_ty_le_cbnv_nghi_viec_11.append(data)
                            if chitieu == 'Chỉ tiêu Quản lý và phát triển con người (Tỷ lệ hoàn thành tháp đào tạo)':
                                if data[0].month == 9:
                                    target_ty_le_hoan_thanh_thap_dao_tao_9.append(data)
                                if data[0].month == 10:
                                    target_ty_le_hoan_thanh_thap_dao_tao_10.append(data)
                                if data[0].month == 11:
                                    target_ty_le_hoan_thanh_thap_dao_tao_11.append(data)

                            # Chỉ tiêu khác
                            if chitieu == 'Số lượng khách hàng hoạt động phát triển mới':
                                if data[0].month == 9:
                                    target_so_luong_kh_moi_9.append(data)
                                if data[0].month == 10:
                                    target_so_luong_kh_moi_10.append(data)
                                if data[0].month == 11:
                                    target_so_luong_kh_moi_11.append(data)
                            if chitieu == 'TOI phí dịch vụ/ 01 khách hàng CN' or chitieu == 'TOI phí dịch vụ khách hàng cá nhân':
                                if data[0].month == 9:
                                    target_toi_phi_dich_vu_khcn_9.append(data)
                                if data[0].month == 10:
                                    target_toi_phi_dich_vu_khcn_10.append(data)
                                if data[0].month == 11:
                                    target_toi_phi_dich_vu_khcn_11.append(data)
                            if chitieu == 'Số lượng khách hàng cá nhân bình quân':
                                if data[0].month == 9:
                                    target_so_luong_khcn_binh_quan_9.append(data)
                                if data[0].month == 10:
                                    target_so_luong_khcn_binh_quan_10.append(data)
                                if data[0].month == 11:
                                    target_so_luong_khcn_binh_quan_11.append(data)
                            if chitieu == 'Tỷ lệ nợ nhóm 2':
                                if data[0].month == 9:
                                    target_ty_le_no_nhom_2_9.append(data)
                                if data[0].month == 10:
                                    target_ty_le_no_nhom_2_10.append(data)
                                if data[0].month == 11:
                                    target_ty_le_no_nhom_2_11.append(data)
                            if chitieu == 'Tỷ lệ nợ xấu':
                                if data[0].month == 9:
                                    target_ty_le_no_xau_9.append(data)
                                if data[0].month == 10:
                                    target_ty_le_no_xau_10.append(data)
                                if data[0].month == 11:
                                    target_ty_le_no_xau_11.append(data)

                result = []

                def sum_data(input_datas):
                    dictdatas = {}
                    # temp_result = []
                    for input_data in input_datas:
                        if not dictdatas:
                            dictdatas = {
                                'PROCESS_DATE' : lib.parseString(input_data[0]),
                                'CHITIEU' : lib.parseString(input_data[1]),
                                'SODU_DS_LK_KYT' : lib.parseFloat(input_data[2]),
                                'THUC_HIEN_KY_T' : lib.parseFloat(input_data[3]),
                                'KE_HOACH_KY_T' : lib.parseFloat(input_data[4]),
                                'TYLE_KY_T' : lib.parseFloat(input_data[5]),
                                'THUC_HIEN_LK' : lib.parseFloat(input_data[6]),
                                'KE_HOACH_LK' : lib.parseFloat(input_data[7]),
                                'TY_LY_LK' : lib.parseFloat(input_data[8]),
                                'DIEM_CHI_TIEU_LK' : lib.parseFloat(input_data[9]),
                                'DIEM_KH_LK' : lib.parseFloat(input_data[10]),
                                'KH_NAM' : lib.parseFloat(input_data[11]),
                                'TY_LE_NAM' : lib.parseFloat(input_data[12]),
                                'DIEM_CHI_TIEU_KH_NAM' : lib.parseFloat(input_data[13]),
                                'DIEM_KH_NAM' : lib.parseFloat(input_data[14]),
                                'AMOUNT_CHART' : lib.parseFloat(input_data[15]),
                                'BRANCH_ID' : "A",
                            }
                        else: 
                            dictdatas['PROCESS_DATE'] = lib.parseString(input_data[0])
                            dictdatas['CHITIEU'] = lib.parseString(input_data[1])
                            dictdatas['SODU_DS_LK_KYT'] = dictdatas['SODU_DS_LK_KYT'] + lib.parseFloat(input_data[2])
                            dictdatas['THUC_HIEN_KY_T'] = dictdatas['THUC_HIEN_KY_T'] + lib.parseFloat(input_data[3])
                            dictdatas['KE_HOACH_KY_T'] = dictdatas['KE_HOACH_KY_T'] + lib.parseFloat(input_data[4])
                            dictdatas['TYLE_KY_T'] = dictdatas['TYLE_KY_T'] + lib.parseFloat(input_data[5])
                            dictdatas['THUC_HIEN_LK'] = dictdatas['THUC_HIEN_LK'] + lib.parseFloat(input_data[6])
                            dictdatas['KE_HOACH_LK'] = dictdatas['KE_HOACH_LK'] + lib.parseFloat(input_data[7])
                            dictdatas['TY_LY_LK'] = dictdatas['TY_LY_LK'] + lib.parseFloat(input_data[8])
                            dictdatas['DIEM_CHI_TIEU_LK'] = dictdatas['DIEM_CHI_TIEU_LK'] + lib.parseFloat(input_data[9])
                            dictdatas['DIEM_KH_LK'] = dictdatas['DIEM_KH_LK'] + lib.parseFloat(input_data[10])
                            dictdatas['KH_NAM'] = dictdatas['KH_NAM'] + lib.parseFloat(input_data[11])
                            dictdatas['TY_LE_NAM'] = dictdatas['TY_LE_NAM'] + lib.parseFloat(input_data[12])
                            dictdatas['DIEM_CHI_TIEU_KH_NAM'] = dictdatas['DIEM_CHI_TIEU_KH_NAM'] + lib.parseFloat(input_data[13])
                            dictdatas['DIEM_KH_NAM'] = dictdatas['DIEM_KH_NAM'] + lib.parseFloat(input_data[14])
                            dictdatas['AMOUNT_CHART'] = dictdatas['AMOUNT_CHART'] + lib.parseFloat(input_data[15])
                            dictdatas['BRANCH_ID'] = "A"

                    # temp_result.append(dictdatas)
                    result.append(dictdatas)

                list_target_param = [
                    target_tang_truong_huy_dong_ckh_9,
                    target_tang_truong_huy_dong_ckh_10,
                    target_tang_truong_huy_dong_ckh_11,
                    target_tang_truong_huy_dong_kkh_9,
                    target_tang_truong_huy_dong_kkh_10,
                    target_tang_truong_huy_dong_kkh_11,
                    target_tang_truong_cho_vay_9,
                    target_tang_truong_cho_vay_10,
                    target_tang_truong_cho_vay_11,
                    target_thu_nhap_thuan_tu_dich_vu_9,
                    target_thu_nhap_thuan_tu_dich_vu_10,
                    target_thu_nhap_thuan_tu_dich_vu_11,
                    target_loi_nhuan_truoc_thue_9,
                    target_loi_nhuan_truoc_thue_10,
                    target_loi_nhuan_truoc_thue_11,
                    target_doanh_so_bao_hiem_nhan_tho_9,
                    target_doanh_so_bao_hiem_nhan_tho_10,
                    target_doanh_so_bao_hiem_nhan_tho_11,
                    target_so_luong_the_TDQT_phat_hanh_moi_9,
                    target_so_luong_the_TDQT_phat_hanh_moi_10,
                    target_so_luong_the_TDQT_phat_hanh_moi_11,
                    target_so_du_trai_phieu_binh_quan_9,
                    target_so_du_trai_phieu_binh_quan_10,
                    target_so_du_trai_phieu_binh_quan_11,
                    target_phat_trien_khach_hang_moi_9,
                    target_phat_trien_khach_hang_moi_10,
                    target_phat_trien_khach_hang_moi_11,
                    target_loi_nhuan_tu_hoat_dong_cap_tin_dung_9,
                    target_loi_nhuan_tu_hoat_dong_cap_tin_dung_10,
                    target_loi_nhuan_tu_hoat_dong_cap_tin_dung_11,
                    target_ty_le_no_nhom_2_phat_sinh_trong_nam_9,
                    target_ty_le_no_nhom_2_phat_sinh_trong_nam_10,
                    target_ty_le_no_nhom_2_phat_sinh_trong_nam_11,
                    target_ty_le_no_xau_phat_sinh_trong_nam_9,
                    target_ty_le_no_xau_phat_sinh_trong_nam_10,
                    target_ty_le_no_xau_phat_sinh_trong_nam_11,
                    target_chi_tieu_chat_luong_dich_vu_9,
                    target_chi_tieu_chat_luong_dich_vu_10,
                    target_chi_tieu_chat_luong_dich_vu_11,
                    target_chi_tieu_quan_ly_rui_ro_9,
                    target_chi_tieu_quan_ly_rui_ro_10,
                    target_chi_tieu_quan_ly_rui_ro_11,
                    target_ty_le_cbnv_nghi_viec_9,
                    target_ty_le_cbnv_nghi_viec_10,
                    target_ty_le_cbnv_nghi_viec_11,
                    target_ty_le_hoan_thanh_thap_dao_tao_9,
                    target_ty_le_hoan_thanh_thap_dao_tao_10,
                    target_ty_le_hoan_thanh_thap_dao_tao_11,
                    target_so_luong_kh_moi_9,
                    target_so_luong_kh_moi_10,
                    target_so_luong_kh_moi_11,
                    target_toi_phi_dich_vu_khcn_9,
                    target_toi_phi_dich_vu_khcn_10,
                    target_toi_phi_dich_vu_khcn_11,
                    target_so_luong_khcn_binh_quan_9,
                    target_so_luong_khcn_binh_quan_10,
                    target_so_luong_khcn_binh_quan_11,
                    target_ty_le_no_nhom_2_9,
                    target_ty_le_no_nhom_2_10,
                    target_ty_le_no_nhom_2_11,
                    target_ty_le_no_xau_9,
                    target_ty_le_no_xau_10,
                    target_ty_le_no_xau_11,
                ]
                for target in list_target_param:
                    sum_data(target)

                print(result)

            cur.close()
            con.close()
            return self.response_success(result, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
