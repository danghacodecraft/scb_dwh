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
                    data_cursor = None

                for data in data_cursor:
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
                        'DIEM_CHITIEU_CHATLUONG_DICHVU': lib.parseFloat(data[27]),
                        'DIEM_XEP_HANG_TUAN_THU': lib.parseFloat(data[28]),
                        'DIEM_CBNV_NGHI_VIEC': lib.parseFloat(data[29]),
                        'DIEM_HOAN_THANH_THAP_DAO_TAO': lib.parseFloat(data[30]),
                        'DIEM_TYLE_NO2_PHATSINH': lib.parseFloat(data[31]),
                        'DIEM_TYLE_NOXAU_PHATSINH': lib.parseFloat(data[32]),
                        'DIEM_KHUYEN_KHICH': lib.parseFloat(data[20]),
                        'TONG_DIEM': lib.parseFloat(data[21]),
                        'DIEU_CHINH_TONG_DIEM': lib.parseFloat(data[22]),
                        'TONG_DIEM_SAU_DIEU_CHINH': lib.parseFloat(data[23]),
                        'XEP_HANG': lib.parseFloat(data[24]),
                        'XEP_LOAI': lib.parseString(data[25]),
                        'PROCESS_DATE': lib.parseString(data[26]),
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
                    data_cursor = None

                for data in data_cursor:
                    if len(data) == 17:
                        val = {
                        'PROCESS_DATE': lib.parseString(data[0]),
                        'CHITIEU': lib.parseString(data[1]),
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
                        'BRANCH_ID': lib.parseString(data[16])
                        }
                        datas.append(val)
                    else:
                        val = {
                            'STT' : lib.parseString(data[0]),
                            'MONTH_ID' : lib.parseString(data[1]),
                            'BRANCH_ID' : lib.parseString(data[2]),
                            'BRANCH_NAME' : lib.parseString(data[3]),
                            'SORT_REGION' : lib.parseString(data[4]),
                            'HE_SO_DIEM_THEO_MO_HINH_DVKD' : lib.parseString(data[5]),
                            'HTKH_LK_TANG_TRUONG_HD' : lib.parseString(data[6]),
                            'DIEM_TANG_TRUONG_HD' : lib.parseString(data[7]),
                            'HTKH_LK_TANG_TRUONG_HDVON_BQ_KKH' : lib.parseString(data[8]),
                            'DIEM_TANG_TRUONG_HDVON_BQ_KKH' : lib.parseString(data[9]),
                            'HTKH_LK_TANG_TRUONG_CHOVAY' : lib.parseString(data[10]),
                            'DIEM_TANG_TRUONG_CHOVAY' : lib.parseString(data[11]),
                            'HTKH_LK_TANG_TRUONG_CHOVAY_BQ' : lib.parseString(data[12]),
                            'DIEM_TANG_TRUONG_CHOVAY_BQ' : lib.parseString(data[13]),
                            'HTKH_LK_THU_PHI_DICH_VU' : lib.parseString(data[14]),
                            'DIEM_THU_PHI_DICH_VU' : lib.parseString(data[15]),
                            'HTKH_LK_THUPHI_DV_BAOGOM_TTQT_LNKDNH' : lib.parseString(data[16]),
                            'DIEM_THUPHI_DV_BAOGOM_TTQT_LNKDNH' : lib.parseString(data[17]),
                            'HTKH_LK_THUPHI_TTQT_LNKDNH' : lib.parseString(data[18]),
                            'DIEM_THUPHI_TTQT_LNKDNH' : lib.parseString(data[19]),
                            'HTKH_LK_DOANHSO_THANHTOAN_QR' : lib.parseString(data[20]),
                            'DIEM_DOANHSO_THANHTOAN_QR' : lib.parseString(data[21]),
                            'HTKH_LK_MERCHANT_QR' : lib.parseString(data[22]),
                            'DIEM_MERCHANT_QR' : lib.parseString(data[23]),
                            'HTKH_LK_DOANHSO_THANHTOAN_POS' : lib.parseString(data[24]),
                            'DIEM_DOANHSO_THANHTOAN_POS' : lib.parseString(data[25]),
                            'HTKH_LK_LOI_NHUAN_TRUOC_THUE' : lib.parseString(data[26]),
                            'DIEM_LOI_NHUAN_TRUOC_THUE' : lib.parseString(data[27]),
                            'HTKH_LK_SLKH_MOI' : lib.parseString(data[28]),
                            'DIEM_SLKH_MOI' : lib.parseString(data[29]),
                            'HTKH_LK_SLHD_EBANKING' : lib.parseString(data[30]),
                            'DIEM_SLHD_EBANKING' : lib.parseString(data[31]),
                            'HTKH_LK_KHMOI_SPVAYTIEN' : lib.parseString(data[32]),
                            'DIEM_KHMOI_SPVAYTIEN' : lib.parseString(data[33]),
                            'HTKH_LK_DOANHSO_BAOLANH' : lib.parseString(data[34]),
                            'DIEM_DOANHSO_BAOLANH' : lib.parseString(data[35]),
                            'HTKH_LK_XULY_NOXAU_THONGTHUONG' : lib.parseString(data[41]),
                            'DIEM_XULY_NOXAU_THONGTHUONG' : lib.parseString(data[42]),
                            'DIEM_CHITIEU_CHATLUONG_DICHVU' : lib.parseString(data[36]),
                            'DIEM_CHITIEU_QLRR' : lib.parseString(data[37]),
                            'DIEM_CBNV_NGHI_VIEC' : lib.parseString(data[38]),
                            'DIEM_TYLE_NO2_PHATSINH' : lib.parseString(data[39]),
                            'DIEM_TYLE_NOXAU_PHATSINH' : lib.parseString(data[40]),
                            'DIEM_KHUYEN_KHICH' : lib.parseString(data[43]),
                            'TONG_DIEM' : lib.parseString(data[44]),
                            'DIEU_CHINHG_TONG_DIEM' : lib.parseString(data[45]),
                            'TONG_DIEM_SAU_DIEU_CHINH' : lib.parseString(data[46]),
                            'XEP_HANG' : lib.parseString(data[47]),
                            'XEP_LOAI' : lib.parseString(data[48]),
                            'PROCESS_DATE' : lib.parseString(data[49]),

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

            key = ""  # ,P_MODULE=>'ket_qua_chi_tieu_ke_hoach'"
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

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_C06_CHART(P_MAN_HINH=>'{}'{}{}{}{}{}) FROM DUAL".format(screen, key,
                                                                                                      division, kv,
                                                                                                      vung, dv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            # lstsum = [
            #     "Doanh số bảo hiểm nhân thọ",
            #     "Số lượng thẻ TDQT phát hành mới",
            #     "Số dư trái phiếu bình quân",
            #     "Phát triển khách hàng mới"
            # ]
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    data_cursor = None

                chi_tieus = {}

                for data in data_cursor:
                    key_chi_tieu = lib.parseString(data[1])
                    key_process_date = str(data[0])
                    branchid = lib.parseString(data[16])
                    if branchid.startswith('V') or branchid.startswith('A'):
                        if key_chi_tieu not in chi_tieus:
                            chi_tieus[key_chi_tieu] = {
                                # 'PROCESS_DATE': lib.parseString(data[0]),
                            }

                        chi_tieu = chi_tieus[key_chi_tieu]
                        if key_process_date not in chi_tieu:
                            chi_tieu[key_process_date] = {
                                'CHITIEU': key_chi_tieu,
                                'PROCESS_DATE': key_process_date,
                                'SODU_DS_LK_KYT': 0,
                                'THUC_HIEN_KY_T': 0,
                                'KE_HOACH_KY_T': 0,
                                'TYLE_KY_T': 0,
                                'THUC_HIEN_LK': 0,
                                'KE_HOACH_LK': 0,
                                'TY_LY_LK': 0,
                                'DIEM_CHI_TIEU_LK': 0,
                                'DIEM_KH_LK': 0,
                                'KH_NAM': 0,
                                'TY_LE_NAM': 0,
                                'DIEM_CHI_TIEU_KH_NAM': 0,
                                'DIEM_KH_NAM': 0,
                                'AMOUNT_CHART': 0,
                                # 'BRANCH_ID': branchid
                            }

                        d = chi_tieu[key_process_date]
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

                for key_chi_tieu in chi_tieus:
                    chi_tieu = chi_tieus[key_chi_tieu]

                    for key_process_date in chi_tieu:
                        d = chi_tieu[key_process_date]

                        d['SODU_DS_LK_KYT'] = lib.parseFloat(d['SODU_DS_LK_KYT'], 2, True)
                        d['THUC_HIEN_KY_T'] = lib.parseFloat(d['THUC_HIEN_KY_T'], 2, True)
                        d['KE_HOACH_KY_T'] = lib.parseFloat(d['KE_HOACH_KY_T'], 2, True)
                        d['TYLE_KY_T'] = lib.parseFloat(d['TYLE_KY_T'], 2, True)
                        d['THUC_HIEN_LK'] = lib.parseFloat(d['THUC_HIEN_LK'], 2, True)
                        d['KE_HOACH_LK'] = lib.parseFloat(d['KE_HOACH_LK'], 2, True)
                        d['TY_LY_LK'] = lib.parseFloat(d['TY_LY_LK'], 2, True)
                        d['DIEM_CHI_TIEU_LK'] = lib.parseFloat(d['DIEM_CHI_TIEU_LK'], 2, True)
                        d['DIEM_KH_LK'] = lib.parseFloat(d['DIEM_KH_LK'], 2, True)
                        d['KH_NAM'] = lib.parseFloat(d['KH_NAM'], 2, True)
                        d['TY_LE_NAM'] = lib.parseFloat(d['TY_LE_NAM'], 2, True)
                        d['DIEM_CHI_TIEU_KH_NAM'] = lib.parseFloat(d['DIEM_CHI_TIEU_KH_NAM'], 2, True)
                        d['DIEM_KH_NAM'] = lib.parseFloat(d['DIEM_KH_NAM'], 2, True)
                        d['AMOUNT_CHART'] = lib.parseFloat(d['AMOUNT_CHART'], 2, True)
                        datas.append(d)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
