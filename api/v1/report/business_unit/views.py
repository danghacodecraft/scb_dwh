import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.report.business_unit.serializers import ChartFResponseSerializer, DataResponseSerializer, CustomerResponseSerializer, RegionInfoResponseSerializer

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
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
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
            sql = """
            select obi.CRM_DWH_PKG.FUN_GET_DATA('{}') 
            FROM DUAL
            """.format(screen)

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
        tags=["BUSINESS"],
        description="""
Screen `C_02_01` DVKD - Tong quan        
- **quan_ly_khach_hang**.
- **tong_so_don_vi**.
- **tong_thu_nhap_thuan**.
- **tong_chi_phi_hoat_dong**.

Screen `C_02_02` DVKD - Chi tiet
- **quan_ly_khach_hang_bdi**.
- **quan_ly_khach_hang_di**.
- **quan_ly_khach_hang_pp**.
- **quan_ly_khach_hang_r**.
- **quan_ly_khach_hang_sli**.
- **quan_ly_khach_hang_p**.
- **quan_ly_khach_hang_n**.
- **quan_ly_khach_hang_sap**.
- **quan_ly_khach_hang_bde**.
- **quan_ly_khach_hang**.
- **quan_ly_khach_hang_d**.
- **quan_ly_khach_hang_g**.
- **quan_ly_khach_hang_pp+**.
- **quan_ly_khach_hang_bd**.
- **quan_ly_khach_hang_de**.
- **quan_ly_khach_hang_ti**.
- **quan_ly_khach_hang_m**.
- **thu_nhap_thuan_tu_dvkh**.
- **thu_nhap_thuan_tu_dich_vu_the_tdqt**.
- **thu_nhap_thuan_tu_dich_vu_the_gn_visa**.
- **thu_nhap_thuan_tu_dich_vu_the_atm**.
- **thu_nhap_thuan_tu_dich_vu_the_may_atm**.
- **thu_nhap_thuan_tu_dich_vu_the_gn_mc**.
- **thu_nhap_thuan_tu_dich_vu_the_pos**.
- **thu_nhap_thuan_tu_dich_vu_the**.
- **thu_nhap_thuan_tu_dich_vu_the_td_mc**.
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

Screen `C_02_03` DVKD - I. Tong hop theo nghiep vu ngan hang
- **tk_thanh_toan_mo_moi**.
- **ebanking_mo_moi**.
- **the_ghi_no_mo_moi**.
- **bao_cao_cif_mo_moi**.
- **the_tin_dung_mo_moi**.

Screen `C_02_04` DVKD - II. Tin dung
- **no_xau**.
- **no_trong_han**.
- **no_qua_han**.

Screen `C_02_05` DVKD - III. Huy dong von
- **huy_dong_von_thi_truong_1**.
- **huy_dong_von_thi_truong_2**.
- **huy_dong_von_vay_nhnn**.

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
                name="dv", type=OpenApiTypes.STR, description="dv"
            )
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: ChartFResponseSerializer(many=True),
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
            dv = ""

            if 'vung' in params.keys():
                vung = ",P_VUNG=>'{vung}'".format(params['vung'])

            if 'dv' in params.keys():
                dv = ",P_DV=>'{dv}'".format(params['dv'])

            sql = """
            select obi.CRM_DWH_PKG.FUN_GET_CHART(
                P_MAN_HINH=>'{}',P_MODULE=>'{}'{}{}
            ) FROM DUAL
            """.format(screen, key, vung, dv)

            #print(sql)
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
                        'unit': data[4],
                        'description': data[5],
                        'type': data[6]
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
- **du_no_nhom_sp**.
- **du_no_td_khcn**.
- **so_luong_khoan_vay**.

Screen `C_03_01`
- **du_no_sp_theo_vung**.
- **don_vi_no_qua_han**.

Screen `C_03_02`
- **vay_san_xuat_kinh_doanh_kh**.
- **vay_san_xuat_kinh_doanh_theo_vung**.
- **vay_bo_sung_vld**.
- **vay_dau_tu_may_moc**.
- **vay_dau_tu_nha_xuong**.
- **vay_san_xuat_kinh_doanh**.

Screen `C_03_03`
- **vay_tieu_dung**.
- **vay_tieu_dung_theo_vung**.
- **vay_tieu_dung_co_tsdb**.
- **vay_tieu_dung_co_tsdb_theo_vung**.
- **vay_thau_chi**.
- **vay_thau_chi_theo_vung**.
- **vay_o_to**.
- **vay_o_to_sl_vay**.
- **vay_o_to_sl_vay_don_vi**.
""",
        parameters=[
            OpenApiParameter(
                name="screen", type=OpenApiTypes.STR, description="screen"
            ),
            OpenApiParameter(
                name="key", type=OpenApiTypes.STR, description="key"
            )
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

            sql = """
                select obi.CRM_DWH_PKG.FUN_GET_CHART_loan(
                    P_MAN_HINH=>'{}',P_MODULE=>'{}'
                ) FROM DUAL
                """.format(screen, key)

            # print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                try:
                    data_cursor = res[0]
                except:
                    print("Loi data ")
                    data_cursor = None

                for row in data_cursor:
                    # for data in row:
                    # val = {
                    #     'periol': data[0],
                    #     'key': lib.create_key(data[1].strip()),
                    #     'label': data[1].strip(),
                    #     'val': data[2],
                    #     'unit': data[4],
                    #     'description': data[5],
                    #     'type': data[6],
                    #     'branch': data[3]
                    # }
                    datas.append(row)

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

            page_number = 1
            if 'page_number' in params.keys():
                page_number = int(params['page_number'])

            page_size = 20
            if 'page_size' in params.keys():
                page_size = int(params['page_size'])

            sql = """
                select obi.CRM_DWH_PKG.FUN_GET_DATA_CUST_VIP(
                    P_MAN_HINH  => '{}',
                    P_VUNG      => 'ALL',
                    P_DV        => 'ALL',
                    P_CCY       => 'VND',
                    P_MODULE    => '{}',
                    P_HANG_VIP  => '{}',
                    P_PAGE_NUM  => {},
                    P_PAGE_SIZE => {}
                ) FROM DUAL
            """.format(screen, key, level, page_number, page_size)
            print(sql)

            # print(sql)
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
                        'MA_KH': data[0],
                        'TEN_KH': data[1],
                        'GIAY_TO_DINH_DANH': data[2],
                        'DIA_CHI': data[3],
                        'DIEN_THOAI': data[4],
                        'EMAIL': data[5],
                        'HANG_KHACH_HANG': data[6],
                        'TONG_TAI_SAN': data[7],
                        'TGCKH': data[8],
                        'TGTT': data[9],
                        'TGKKH': data[10],
                        'THE_TIN_DUNG': data[11],
                        'DU_NO_VAY': data[12],
                        'NV_QL_MA': data[13],
                        'NV_QL_TEN': data[14],
                        'NV_QL_EMAIL': data[15],
                        'NV_QL_SO_DT': data[16],
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
            screen = params['screen']
            region = params['region']

            sql = """
                select obi.CRM_DWH_PKG.FUN_GET_REGION_MANA_INFO(
                    P_MAN_HINH=>'{}',p_vung =>'{}'
                ) FROM DUAL
            """.format(screen, region)
            print(sql)

            # print(sql)
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
                        'address': data[0],
                        'fullname': data[1],
                        'email': data[2],
                        'mobile': data[3],
                        'fullname_op': data[4],
                        'email_op': data[5],
                        'mobile_op': data[6]
                    }
                    datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)