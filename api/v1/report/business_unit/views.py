import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import datetime
import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.business_unit.serializers import ChartFResponseSerializer, ChartResponseSerializer, DataResponseSerializer, \
    CustomerResponseSerializer, RegionInfoResponseSerializer, BranchInfoResponseSerializer

class BusinessUnitView(BaseAPIView):
    @extend_schema(
        operation_id='Data',
        summary='List',
        tags=["BUSINESS"],
        description="""
The `Screen` has values: 
- **C_02_01**. DVKD - Tong quan
- **C_02_02**. DVKD - Chi tiet
- **C_02_03**. DVKD - I. Tong hop theo nghiep vu ngan hang
- **C_02_04**. DVKD - II. Tin dung
- **C_02_05**. DVKD - III. Huy dong von
- **C_02_05_01**. DVKD - IV. Tong thu nhap thuan - 1. Thu nhap tu tin dung
- **C_02_05_02**. DVKD - IV. Tong thu nhap thuan - 2. Thu nhap tu von huy dong 
- **C_02_05_03**. DVKD - IV. Tong thu nhap thuan - 3. Thu nhap tu thi truong
- **C_02_05_04_01**. DVKD - IV. Tong thu nhap thuan - 4. Thu nhap tu von huy dong
- **C_02_05_04_02**. DVKD - IV. Tong thu nhap thuan - 4. Thu nhap tu von huy dong
- **C_02_05_05**. DVKD - IV. Tong thu nhap thuan - 5. Thu nhap thuan tu kinh doanh
- **C_02_05_06**. DVKD - IV. Tong thu nhap thuan - 6. Thu nhap thuan tu kdnh
- **C_02_05_07**. DVKD - IV. Tong thu nhap thuan - 7. Thu nhap thuan tu hoat dong
- **C_02_05_08**. DVKD - IV. Tong thu nhap thuan - 8. Thu nap thuan tu hoat dong
- **C_03**.
- **C_04**.
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
            OpenApiParameter(
                name="fdate", type=OpenApiTypes.STR, description="fdate"
            ),
            OpenApiParameter(
                name="tdate", type=OpenApiTypes.STR, description="tdate"
            ),
            OpenApiParameter(
                name="division", type=OpenApiTypes.STR, description="division"
            )
        ],
        responses={
            status.HTTP_201_CREATED: DataResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def data(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            screen = params['screen']

            vung = ""
            if 'vung' in params.keys():
                vung = ",P_VUNG=>'{}'".format(params['vung'])

            kv = ""
            if 'kv' in params.keys():
                kv = ",P_KV=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            fdate = ""
            if 'fdate' in params.keys():
                fdate = ",P_FDATE=>'{}'".format(params['fdate'])

            tdate = ""
            if 'tdate' in params.keys():
                tdate = ",P_TDATE=>'{}'".format(params['tdate'])

            division = ""
            if 'division' in params.keys():
                division = ",P_DIVISION=>'{}'".format(params['division'])

            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_DATA('{}'{}{}{}{}{}{}) FROM DUAL".format(screen, vung, kv, dv, fdate, tdate, division)
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

                dd = {}
                for data in data_cursor:
                    print(data)
                    # ('0-0-A-11.3', 'Huy động vốn', 576838903156, 2288694126853, 576838903156, 576838903156, 'Huy động vốn bình quân', 'BQ', 2288694126853, 'K01', 'KV HCM1', 'KHCN')
                    title = lib.parseString(data[6])
                    ids = lib.create_key(title)
                    if ids == "so_luong_khach_hang":
                        division = data[11]
                        if division == "KHDN":
                            title = "Khách hàng doanh nghiệp"
                            ids = lib.create_key(title)
                        elif division == "KHCN":
                            title = "Khách hàng cá nhân"
                            ids = lib.create_key(title)
                        elif division == "KHAC":
                            title = "Khách hàng tổ chức tín dụng"
                            ids = lib.create_key(title)

                    if ids not in dd:
                        dd[ids] = {
                            'code': data[0],
                            'id': ids,
                            "title": title,
                            'unit': lib.parseString(data[7]),
                            'day': lib.parseFloat(data[2]),
                            'week': lib.parseFloat(data[3]),
                            'month': lib.parseFloat(data[4]),
                            'accumulated': lib.parseFloat(data[5]),
                            'AMT_KY_TRUOC': lib.parseFloat(data[8]),
                        }
                    else:
                        d = dd[ids]
                        d['day'] = d['day'] + lib.parseFloat(data[2])
                        d['week'] = d['week'] + lib.parseFloat(data[3])
                        d['month'] = d['month'] + lib.parseFloat(data[4])
                        d['accumulated'] = d['accumulated'] + lib.parseFloat(data[5])
                        d['AMT_KY_TRUOC'] = d['AMT_KY_TRUOC'] + lib.parseFloat(data[8])

                for ids in dd:
                    datas.append(dd[ids])

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
        tags=["BUSINESS"],
        description="""
 `Sum` default 1        
- **0**.
- **1**.
        
Screen `C_02_01` DVKD - Tong quan        
- **quan_ly_khach_hang**.
- **tong_so_don_vi**.
- **tong_thu_nhap_thuan**.
- **tong_chi_phi_hoat_dong**.

Screen `C_02_02` DVKD - Chi tiet
- **quan_ly_khach_hang**.
- **quan_ly_khach_hang_r**.
- **quan_ly_khach_hang_sli**.
- **quan_ly_khach_hang_sap**.
- **quan_ly_khach_hang**.
- **quan_ly_khach_hang_d**.
- **quan_ly_khach_hang_di**.
- **quan_ly_khach_hang_de**.
- **quan_ly_khach_hang_g**.
- **quan_ly_khach_hang_p**.
- **quan_ly_khach_hang_pp**.
- **quan_ly_khach_hang_pp+**.
- **quan_ly_khach_hang_bd**.
- **quan_ly_khach_hang_bdi**.
- **quan_ly_khach_hang_bde**.
- **quan_ly_khach_hang_ti**.
- **quan_ly_khach_hang_n**.
- **quan_ly_khach_hang_m**.
- **thu_nhap_thuan_tu_dvkh**.
- **thu_nhap_thuan_tu_dich_vu_the**.
- **thu_nhap_thuan_tu_dich_vu_the_atm**.
- **thu_nhap_thuan_tu_dich_vu_the_tdqt**.
- **thu_nhap_thuan_tu_dich_vu_the_td_mc**.
- **thu_nhap_thuan_tu_dich_vu_the_gn_visa**.
- **thu_nhap_thuan_tu_dich_vu_the_gn_mc**.
- **thu_nhap_thuan_tu_dich_vu_the_may_atm**.
- **thu_nhap_thuan_tu_dich_vu_the_pos**.
- **tong_chi_phi_hoat_dong_tai_san**.
- **tong_chi_phi_hoat_dong_nhan_vien**.
- **tong_chi_phi_hoat_dong_thue**.
- **tong_chi_phi_hoat_dong_tien_gui**.
- **tong_so_don_vi**.
- **tong_thu_nhap_thuan**.
- **tong_chi_phi_hoat_dong**.
- **tong_chi_phi_hoat_dong_hoat_dong**.
- **tong_chi_phi_hoat_dong_dau_tu**.
- **bao_cao_cif_mo_moi**.
- **huy_dong_von**.
- **cho_vay_khach_hang**.
- **cho_vay_khach_hang_chi_tiet**.

Screen `C_02_03` DVKD - I. Tong hop theo nghiep vu ngan hang
- **tk_thanh_toan_mo_moi**.
- **the_ghi_no_mo_moi**.
- **the_tin_dung_mo_moi**.
- **ebanking_mo_moi**.
- **bao_cao_cif_mo_moi**.

Screen `C_02_04` DVKD - II. Tin dung
- **no_xau**.
- **no_trong_han**.
- **no_qua_han**.

Screen `C_02_05` DVKD - III. Huy dong von
- **huy_dong_von_vay_nhnn**.
- **huy_dong_von_thi_truong_1**.
- **huy_dong_von_thi_truong_2**.

Screen `C_02_05_01` DVKD - IV. Tong thu nhap thuan - 1. Thu nhap tu tin dung
- **thu_nhap_thuan_cho_vay**.
- **hoat_dong_tin_dung_khac**.
- **tong_thu_nhap_thuan**.


Screen `C_02_05_02` DVKD - IV. Tong thu nhap thuan - 2. Thu nhap tu von huy dong 
- **huy_dong_tt1**.
- **tong_thu_nhap_thuan**.

Screen `C_02_05_03` DVKD - IV. Tong thu nhap thuan - 3. Thu nhap tu thi truong
- **trung_tam_von_alm**.
- **trung_tam_von_fpt**.
- **tong_thu_nhap_thuan**.
- **thu_nhap_thuan_tt2**.

Screen `C_02_05_04_01` DVKD - IV. Tong thu nhap thuan - 4. Thu nhap tu von huy dong
- **thu_nhap_thuan_tu_dvkh**.
- **thu_nhap_thuan_tu_dich_vu_the**.
- **thu_nhap_thuan_tu_dich_vu_the_atm**.
- **thu_nhap_thuan_tu_dich_vu_the_gn_mc**.
- **thu_nhap_thuan_tu_dich_vu_the_may_atm**.
- **thu_nhap_thuan_tu_dich_vu_the_gn_visa**.
- **thu_nhap_thuan_tu_dich_vu_the_td_mc**.
- **thu_nhap_thuan_tu_dich_vu_the_pos**.
- **thu_nhap_thuan_tu_dich_vu_the_tdqt**.
- **thu_nhap_thuan_tu_dich_vu_the_td_visa**.
- **thu_nhap_thuan_dich_vu_the**.
- **thu_nhap_thuan_dich_vu_atm**.
- **thu_nhap_thuan_dich_vu_thanh_toan**.
- **thu_nhap_thuan_dich_vu_ngan_hang_dien_tu**.
- **thu_nhap_thuan_dich_vu_ngan_quy_tien_mat**.
- **thu_nhap_thuan_dich_vu_dai_ly_bao_hiem**.
- **thu_nhap_thuan_dich_vu_thuong_mai_dien_tu**.
- **thu_nhap_thuan_dich_vu_tai_khoan_tien_gui**.
- **tong_thu_nhap_thuan**.

Screen `C_02_05_04_02` DVKD - IV. Tong thu nhap thuan - 4. Thu nhap tu von huy dong
- **thu_nhap_thuan_dich_vu_dong_dau_tu**.
- **thu_nhap_thuan_dich_vu_thanh_toan**.
- **thu_nhap_thuan_dich_vu_bao_lanh**.
- **thu_nhap_thuan_dich_vu_tin_dung**.
- **thu_nhap_thuan_dich_vu_tu_van**.
- **thu_nhap_thuan_dich_vu_quy_mo**.
- **thu_nhap_thuan_dich_vu_khac**.

Screen `C_02_05_05` DVKD - IV. Tong thu nhap thuan - 5. Thu nhap thuan tu kinh doanh
- **tong_thu_nhap_thuan**.
- **kinh_doanh_tien_te**.

Screen `C_02_05_06` DVKD - IV. Tong thu nhap thuan - 6. Thu nhap thuan tu kdnh
- **thu_nhap_thuan_kdnh**.
- **tong_thu_nhap_thuan**.

Screen `C_02_05_07` DVKD - IV. Tong thu nhap thuan - 7. Thu nhap thuan tu hoat dong
- **dau_tu_khac**.
- **trai_phieu_vamc**.
- **tong_thu_nhap_thuan**.

Screen `C_02_05_08` DVKD - IV. Tong thu nhap thuan - 8. Thu nap thuan tu hoat dong
- **tong_thu_nhap_thuan**.
- **hoat_dong_khac**.

""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="key", type=OpenApiTypes.STR, description="key"
            ),
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
            OpenApiParameter(
                name="fdate", type=OpenApiTypes.STR, description="fdate"
            ),
            OpenApiParameter(
                name="tdate", type=OpenApiTypes.STR, description="tdate"
            ),
            OpenApiParameter(
                name="division", type=OpenApiTypes.STR, description="division"
            ),
            OpenApiParameter(
                name="sum", type=OpenApiTypes.STR, description="sum"
            )
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
            # serializer = ChartFRequestSerializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            #
            # name = serializer.validated_data['name']
            # region = serializer.validated_data['region']
            # unit = serializer.validated_data['unit']
            con, cur = lib.connect()

            params = request.query_params.dict()
            screen = params['screen']
            key = params['key']

            vung = ""
            kv = ""
            if 'vung' in params.keys():
                vung = ",P_VUNG=>'{}'".format(params['vung'])
            elif 'kv' in params.keys():
                kv = ",P_VUNG=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            fdate = ""
            if 'fdate' in params.keys():
                fdate = ",P_FDATE=>'{}'".format(params['fdate'])

            tdate = ""
            if 'tdate' in params.keys():
                dv = ",P_TDATE=>'{}'".format(params['tdate'])

            division = ""
            if 'division' in params.keys():
                division = ",P_DIVISION=>'{}'".format(params['division'])

            sum = "1"
            if 'sum' in params.keys():
                sum = params['sum']

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_CHART( P_MAN_HINH=>'{}',P_MODULE=>'{}'{}{}{}{}{}{} ) FROM DUAL".format(screen, key, vung, kv, dv, fdate, tdate, division)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]

                if sum == "1":
                    dicdatas = {}

                    if key == "quan_ly_khach_hang":
                        dicdatas['khach_hang_doanh_nghiep_khoi_dn'] = {
                            'key': 'khach_hang_doanh_nghiep_khoi_dn',
                            'label': "Khách hàng doanh nghiệp khối DN",
                            'unit': "khách hàng",
                            'description': "khách hàng",
                            'type': "khách hàng",
                            'AMT_KY_TRUOC': "",
                            'val': 0,
                            'LK_NAM': 0,
                        }
                        dicdatas['khach_hang_ca_nhan_khoi_pfs'] = {
                            'key': 'khach_hang_ca_nhan_khoi_pfs',
                            'label': "Khách hàng cá nhân khối PFS",
                            'unit': "khách hàng",
                            'description': "khách hàng",
                            'type': "khách hàng",
                            'AMT_KY_TRUOC': "",
                            'val': 0,
                            'LK_NAM': 0,
                        }

                    for data in data_cursor:
                        # print(data)
                        keydata = lib.create_key(data[1])
                        loaikh = lib.parseString(data[13]) if len(data) > 13 else ""
                        if keydata not in dicdatas:
                            dicdatas[keydata] = {
                                'key': keydata,
                                'label': lib.parseString(data[1]),
                                'unit': lib.parseString(data[4]),
                                'description': lib.parseString(data[5]),
                                'type': lib.parseString(data[6]),
                                'AMT_KY_TRUOC': lib.parseString(data[8]),

                                'val': lib.parseFloat(data[2], 2, False),
                                'LK_NAM': lib.parseFloat(data[10], 2, False),
                            }
                        else:
                            d = dicdatas[keydata]
                            d['val'] = d['val'] + lib.parseFloat(data[2], 2, False)
                            d['LK_NAM'] = d['LK_NAM'] + lib.parseFloat(data[10], 2, False)

                        if key == "quan_ly_khach_hang":
                            if loaikh == 'A':
                                d = dicdatas['khach_hang_ca_nhan_khoi_pfs']
                                d['val'] = d['val'] + lib.parseFloat(data[2], 2, False)
                                d['LK_NAM'] = d['LK_NAM'] + lib.parseFloat(data[10], 2, False)
                            elif loaikh == 'B':
                                d = dicdatas['khach_hang_doanh_nghiep_khoi_dn']
                                d['val'] = d['val'] + lib.parseFloat(data[2], 2, False)
                                d['LK_NAM'] = d['LK_NAM'] + lib.parseFloat(data[10], 2, False)

                    for k in dicdatas:
                        dicdatas[k]['val'] = lib.parseFloat(dicdatas[k]['val'], 2, True)
                        dicdatas[k]['LK_NAM'] = lib.parseFloat(dicdatas[k]['LK_NAM'], 2, True)
                        datas.append(dicdatas[k])

                else:
                    for data in data_cursor:
                        print(data)
                        key = lib.create_key(data[1])
                        value = lib.parseFloat(data[2], 2, False)
                        LK_NAM = lib.parseFloat(data[10], 2, False)
                        #('0-0-B-10.10', 'Thu nhập từ hoạt động KDNH', 0, 'Thu nhập từ hoạt động KDNH', None, None, 'Toàn hàng', None, 0, 0)
                        val = {
                            'key': key,
                            'label': lib.parseString(data[1]),
                            'unit': lib.parseString(data[4]),
                            'description': lib.parseString(data[5]),
                            'type': lib.parseString(data[6]),
                            'AMT_KY_TRUOC': lib.parseString(data[8]),

                            'val': value,
                            'LK_NAM': LK_NAM,

                            'LOAI_KH': lib.parseString(data[13]) if len(data) > 13 else "",
                            'BRANCH': lib.parseString(data[14]) if len(data) > 14 else "",
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
        operation_id='Chart Loan',
        summary='List',
        tags=["BUSINESS"],
        description="""
Screen `C_03` 
- **du_no_td_khcn**.
- **du_no_nhom_sp**.
- **du_no_vay_theo_nam**.
- **so_luong_khoan_vay**.

Screen `C_03_01` 
- **don_vi_no_qua_han**.
- **du_no_sp_theo_vung**.

Screen `C_03_02` 
- **vay_bo_sung_vld**.
- **vay_bo_sung_vld_theo_vung**.
- **vay_dau_tu_may_moc**.
- **vay_dau_tu_may_moc_theo_vung**.
- **vay_dau_tu_nha_xuong**.
- **vay_dau_tu_nha_xuong_theo_vung**.
- **vay_san_xuat_kinh_doanh**.
- **vay_san_xuat_kinh_doanh_kh**.
- **vay_san_xuat_kinh_doanh_theo_vung**.
- **sl_vay_bo_sung_vld**.
- **sl_vay_dau_tu_nha_xuong**.
- **sl_vay_dau_tu_may_moc**.
- **sl_vay_san_xuat_kinh_doanh**.

Screen `C_03_03` 
- **vay_o_to**.
- **vay_o_to_theo_vung**.
- **vay_o_to_sl_vay**.
- **vay_o_to_sl_vay_don_vi**.
- **vay_thau_chi**.
- **vay_thau_chi_theo_vung**.
- **vay_tieu_dung**.
- **vay_tieu_dung_theo_vung**.
- **vay_tieu_dung_co_tsdb**.
- **vay_tieu_dung_co_tsdb_theo_vung**.
- **vay_nong_nghiep**.
- **vay_nong_nghiep_theo_vung**.
- **sl_vay_nong_nghiep**.
- **sl_vay_tieu_dung_co_tsdb**.

Screen `C_03_04` 
- **vay_o_to**.
- **vay_thau_chi**.
- **vay_tieu_dung_co_tsdb**.
- **vay_tieu_dung_khong_tsdb**.
- **vay_tieu_dung_khong_tsdb_theo_vung**.
- **so_luong_tai_khoan_vay_thau_chi**.
- **so_luong_tai_khoan_vay_tieu_dung**.
- **sl_vay_thau_chi**.
- **sl_vay_tieu_dung_khong_tsdb**.

Screen `C_03_05` program `TOPUP` 
- **vay_theo_chuong_trinh**.
- **so_luong_tk_vay_theo_chuong_trinh**.

Screen `C_03_06` program `SLH` 
- **vay_theo_chuong_trinh**.
- **so_luong_tk_vay_theo_chuong_trinh**.

Screen `C_03_07` program `DQV` 
- **vay_theo_chuong_trinh**.
- **so_luong_tk_vay_theo_chuong_trinh**.

Screen `C_03_08` program `VUD` 
- **vay_theo_chuong_trinh**.
- **so_luong_tk_vay_theo_chuong_trinh**.

""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="key", type=OpenApiTypes.STR, description="key"
            ),
            OpenApiParameter(
                name="program", type=OpenApiTypes.STR, description="program"
            ),
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
            OpenApiParameter(
                name="year", type=OpenApiTypes.STR, description="year"
            ),
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: ChartFResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def chart_loan(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            screen = params['screen']
            key = params['key']

            program = ""
            if 'program' in params.keys():
                program = ", p_program=>'{}'".format(params['program'])

            vung = ""
            if 'vung' in params.keys():
                vung = ",P_VUNG=>'{}'".format(params['vung'])

            dv = ""
            if 'dv' in params.keys():
                dv = ",P_DV=>'{}'".format(params['dv'])

            year = ",P_YEAR=>'ALL_YEAR'"
            if 'year' in params.keys():
                py = params['year']
                if py != 'ALL_YEAR':
                    year = ",P_YEAR=>'{}'".format(py)

            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_CHART_loan( P_MAN_HINH=>'{}',P_MODULE=>'{}'{}{}{}{} ) FROM DUAL".format(screen, key, program, vung, dv, year)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    # y = data[13] if len(data) > 13 else None
                    # if py != 'ALL_YEAR' and y is not None and y != py:
                    #     continue

                    val = {
                        'TIEU_DE': lib.parseString(data[0]),
                        'CO_TSDB': lib.parseString(data[1]),
                        'UNIT': lib.parseString(data[2]),
                        'BR': lib.parseString(data[3]),
                        'KH': lib.parseString(data[4]),
                        'DU_NO': lib.parseFloat(data[5]),
                        'DU_NO_XAU': lib.parseFloat(data[6]),
                        'DU_NO_QUA_HAN': lib.parseFloat(data[7]),
                        'TY_LE_DU_NO_XAU': lib.parseFloat(data[8]),
                        'TY_LE_DU_NO_QUA_HAN': lib.parseFloat(data[9]),
                        'TY_LE_DU_NO': lib.parseFloat(data[10]),
                        'PROGRAM_ID': lib.parseString(data[11]),
                        'USING_DETAIL': lib.parseString(data[12]),
                        'LK_NAM': lib.parseString(data[13]) if len(data) > 13 else None
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
        operation_id='Customer Vip',
        summary='List',
        tags=["BUSINESS"],
        description="""
Param `screen`         
- **C_02_02**.

Param `cust_type`         
- **C** TỔ CHỨC.
- **I** CÁ NHÂN.
- **ALL** ALL KH HÉN.

Param `key`         
- **danh_sach_kh_vip**.

Param `level`         
- **SILVER**.
- **GOLD**.
- **TITANIUM**.
- **PLATINUM**.
- **PLATINUM PLUS**.
- **SAPPHIRE**.
- **SAPPHIRE EXPERIENCE**.
- **DIAMOND**.
- **DIAMOND FAMILY**.
- **DIAMOND INFLUENCE**.
- **DIAMOND EXPERIENCE**.
- **BLUE DIAMOND**.
- **BLUE DIAMOND FAMILY**.
- **BLUE DIAMOND INFLUENCE**.
- **BLUE DIAMOND INFLUENCE**.
- **RUBY**.
- **RUBY FAMILY**.
- **RUBY EXPERIENCE**.

Param `page_number` default = 0
Param `page_size` default = 20
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="key", type=OpenApiTypes.STR, description="key"
            ),
            OpenApiParameter(
                name="level", type=OpenApiTypes.STR, description="level"
            ),
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            ),
            OpenApiParameter(
                name="cust_type", type=OpenApiTypes.STR, description="cust_type"
            ),
            OpenApiParameter(
                name="page_number", type=OpenApiTypes.STR, description="page_number"
            ),
            OpenApiParameter(
                name="page_size", type=OpenApiTypes.STR, description="page_size"
            )
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: CustomerResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def customer(self, request):
        try:
            # serializer = ChartFRequestSerializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            #
            # name = serializer.validated_data['name']
            # region = serializer.validated_data['region']
            # unit = serializer.validated_data['unit']
            con, cur = lib.connect()

            params = request.query_params.dict()
            screen = params['screen']
            key = params['key']
            level = params['level']

            vung = "ALL"
            if 'vung' in params.keys():
                vung = params['vung']

            dv = "ALL"
            if 'dv' in params.keys():
                dv = params['dv']

            cust_type = ""
            if 'cust_type' in params.keys():
                cust_type = params['cust_type']

            page_number = 1
            if 'page_number' in params.keys():
                page_number = int(params['page_number'])

            page_size = 20
            if 'page_size' in params.keys():
                page_size = int(params['page_size'])

            sql = """
                SELECT obi.CRM_DWH_PKG.FUN_GET_DATA_CUST_VIP(
                    P_MAN_HINH  => '{}',
                    P_VUNG      => '{}',
                    P_DV        => '{}',
                    P_CCY       => 'VND',
                    P_MODULE    => '{}',
                    P_CUST_TYPE => '{}',
                    P_HANG_VIP  => '{}',
                    P_PAGE_NUM  => {},
                    P_PAGE_SIZE => {}
                ) FROM DUAL
            """.format(screen, vung, dv, key, cust_type, level, page_number, page_size)
            # sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_DATA_CUST_VIP( P_MAN_HINH=>'C_02_02',P_HANG_VIP=>'GOLD',P_CUST_TYPE=>'C',P_VUNG => 'V01') FROM DUAL"
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
                        'MA_KH': lib.parseString(data[0]),
                        'TEN_KH': lib.parseString(data[1]),
                        'GIAY_TO_DINH_DANH': lib.parseString(data[2]),
                        'DIA_CHI': lib.parseString(data[3]),
                        'DIEN_THOAI': lib.parseString(data[4]),
                        'EMAIL': lib.parseString(data[5]),
                        'HANG_KHACH_HANG': lib.parseString(data[6]),
                        'TONG_TAI_SAN': lib.parseFloat(data[7]),
                        'TGCKH': lib.parseFloat(data[8]),
                        'TGTT': lib.parseFloat(data[9]),
                        'TGKKH': lib.parseFloat(data[10]),
                        'THE_TIN_DUNG': lib.parseString(data[11]),
                        'DU_NO_VAY': lib.parseFloat(data[12]),
                        'NV_QL_MA': lib.parseString(data[13]),
                        'NV_QL_TEN': lib.parseString(data[14]),
                        'NV_QL_EMAIL': lib.parseString(data[15]),
                        'NV_QL_SO_DT': lib.parseString(data[16])
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
        operation_id='Region Info',
        summary='List',
        tags=["BUSINESS"],
        description="""
Param `screen`         
- **TRANG_CHU**.
- **C_02_02**.

Param `region`         
- **VÙNG 02**.
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="region", type=OpenApiTypes.STR, description="region"
            )
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: RegionInfoResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def region(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()

            screen = 'TRANG_CHU'
            if 'screen' in params.keys():
                screen = params['screen']

            region = "VÙNG 02"
            if 'region' in params.keys():
                region = params['region']

            sql = "SELECT OBI.CRM_DWH_PKG.FUN_GET_REGION_MANA_INFO(P_MAN_HINH=>'{}', P_VUNG=>'{}', P_DV=>'ALL', P_CCY=>'ALL', P_MODULE=>'ALL' ) FROM DUAL".format(screen, region)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    val = {
                        'address': lib.parseString(data[0]),
                        'fullname': lib.parseString(data[1]),
                        'email': lib.parseString(data[2]),
                        'mobile': lib.parseString(data[3]),
                        "user": lib.parseUser(data[2]),
                        'fullname_op': lib.parseString(data[4]),
                        'email_op': lib.parseString(data[5]),
                        'mobile_op': lib.parseString(data[6]),
                        "user_op": lib.parseUser(data[5]),
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
        operation_id='Branch Info',
        summary='List',
        tags=["BUSINESS"],
        description="""
Param `screen`         
- **TRANG_CHU**.
- **C_02_02**.

Param `dv`         
- **001**.
    """,
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="dv", type=OpenApiTypes.STR, description="dv"
            )
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: BranchInfoResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def branch(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()

            screen = 'TRANG_CHU'
            if 'screen' in params.keys():
                screen = params['screen']

            dv = params['dv']

            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_BRN_MANA_INFO(P_MAN_HINH=>'{}', P_VUNG=>'ALL', P_DV=>'{}', P_CCY=>'ALL', P_MODULE=>'ALL' ) FROM DUAL".format(screen, dv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    #('7/57D Nguyễn Khắc Nhu,Phường Cô Giang,Quận 1,Long An,Việt Nam', 'TRỊNH BÁ VƯƠNG', 'VUONGTB@SCB.COM.VN', '+84 939292368', '001')
                    val = {
                        'address': data[0],
                        'fullname': data[1],
                        'email': data[2],
                        'mobile': data[3],
                        "user": lib.parseUser(data[2]),
                        "id": data[4],
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)