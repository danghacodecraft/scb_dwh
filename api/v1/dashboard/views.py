import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

import json
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.dashboard.serializers import DataResponseSerializer, ChartResponseSerializer


class DashboardView(BaseAPIView):
    @extend_schema(
        operation_id='Data',
        summary='List',
        tags=["Dashboard"],
        description="""
The `vung` example: 
- **V02**.

The `kv` example: 
- **K01**.

The `dv` example: 
- **001**.

The `division` example: 
- **A**. khối PFS
- **B**. khối DOANH NGHIỆP

""",
        parameters=[
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
                name="division", type=OpenApiTypes.STR, description="division"
            ),
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

            # print(cx_Oracle.version)
            # print("Database version:", con.version)
            # print("Client version:", cx_Oracle.clientversion())
            params = request.query_params.dict()
            vung = ""
            if 'vung' in params.keys():
                vung = ", P_VUNG=>'{}'".format(params['vung'])

            kv = ""
            if 'kv' in params.keys():
                kv = ", P_KV=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ", P_DV=>'{}'".format(params['dv'])

            division = ""
            if 'division' in params.keys():
                division = ", P_DIVISION=>'{}'".format(params['division'])

            # ds = [
            #     'tong_tai_san',
            #     'ho_so_vay',
            #     'no_xau_dn'
            #     'no_xau_pfs'
            #     'tong_du_no_tin_dung'
            #     'tong_huy_dong'
            #     'tong_chi_phi_hoat_dong'
            #     'loi_nhuan_truoc_thue'
            # ]
            # call the function
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_DATA('TRANG_CHU'{}{}{}) FROM DUAL".format(vung, dv, division)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                dicdatas = {}
                for data in data_cursor:
                    #ID, NAME, AMT_DAY, AMT_WEEK, AMT_MONTH, AMT_YEAR, TIEU_DE, UNIT, AMT_KY_TRUOC
                    print(data)

                    if kv != "" and kv != data[9]:
                        continue

                    title = lib.parseString(data[6])
                    ids = lib.create_key(title)
                    if ids == "tong_so_khach_hang_moi":
                        division = data[11]
                        if division == "KHDN":
                            title = "Tổng số khách hàng mới khối dn"
                        elif division == "KHCN":
                            title = "Tổng số khách hàng mới khối pfs"
                        elif division == "KHAC":
                            title = "Tổng số Khách hàng mới tín dụng"
                        ids = lib.create_key(title)

                    elif ids == "so_luong_khach_hang":
                        division = data[11]
                        if division == "KHDN":
                            title = "Tổng số khách hàng khối dn"
                        elif division == "KHCN":
                            title = "Tổng số khách hàng khối pfs"
                        elif division == "KHAC":
                            title = "Tổng số Khách hàng tín dụng"
                        ids = lib.create_key(title)

                    elif ids == "tang_giam_tong_so_khach_hang_moi":
                        division = data[11]
                        if division == "KHDN":
                            title = "Tăng giảm tổng số khách hàng mới khối dn"
                        elif division == "KHCN":
                            title = "Tăng giảm tổng số khách hàng mới khối pfs"
                        elif division == "KHAC":
                            title = "Tăng giảm tổng số khách hàng mới tín dụng"
                        ids = lib.create_key(title)

                    elif ids == "no_xau":
                        division = data[11]
                        if division == "KHDN":
                            title = "Nợ xấu DN"
                        elif division == "KHCN":
                            title = "Nợ xấu pfs"
                        elif division == "KHAC":
                            title = "Nợ xấu tín dụng"
                        ids = lib.create_key(title)

                    elif ids == "tang_giam_no_xau" or ids == "so_luong_no_xau_pfs":
                        division = data[11]
                        if division == "KHDN":
                            title = "Số lượng nợ xấu DN"
                        elif division == "KHCN":
                            title = "Số lượng nợ xấu pfs"
                        elif division == "KHAC":
                            title = "Số lượng nợ xấu tín dụng"
                        ids = lib.create_key(title)

                    if ids not in dicdatas:
                        dicdatas[ids] = {
                            'code': data[0],
                            'id': ids,
                            "title": lib.parseString(data[6]),
                            'unit': lib.parseString(data[7]),

                            'day': lib.parseFloat(data[2], 2, False),
                            'week': lib.parseFloat(data[3], 2, False),
                            'month': lib.parseFloat(data[4], 2, False),
                            'accumulated': lib.parseFloat(data[5], 2, False),
                            'amt_year': lib.parseFloat(data[5], 2, False),
                            'amt_ky_truoc': lib.parseFloat(data[8], 2, False),
                            'divisor_bal_lcl': lib.parseFloat(data[12], 2, False),
                            'divider_bal_lcl': lib.parseFloat(data[13], 2, False)
                        }
                    else:
                        d = dicdatas[ids]
                        d['day'] = lib.parseFloat(d['day'] + lib.parseFloat(data[2], 2, False))
                        d['week'] = lib.parseFloat(d['week'] + lib.parseFloat(data[3], 2, False))
                        d['month'] = lib.parseFloat(d['month'] + lib.parseFloat(data[4], 2, False))
                        d['accumulated'] = lib.parseFloat(d['accumulated'] + lib.parseFloat(data[5], 2, False))
                        d['amt_year'] = lib.parseFloat(d['amt_year'] + lib.parseFloat(data[5], 2, False))
                        d['amt_ky_truoc'] = lib.parseFloat(d['amt_ky_truoc'] + lib.parseFloat(data[8], 2, False))
                        d['divisor_bal_lcl'] = d['divisor_bal_lcl'] + lib.parseFloat(data[12], 2, False)
                        d['divider_bal_lcl'] = d['divider_bal_lcl'] + lib.parseFloat(data[13], 2, False)

                for ids in dicdatas:
                    d = dicdatas[ids]
                    d['day'] = lib.parseFloat(d['day'], 2, True)
                    d['week'] = lib.parseFloat(d['week'], 2, True)
                    d['month'] = lib.parseFloat(d['month'], 2, True)
                    d['accumulated'] = lib.parseFloat(d['accumulated'], 2, True)
                    d['amt_year'] = lib.parseFloat(d['amt_year'], 2, True)
                    d['amt_ky_truoc'] = lib.parseFloat(d['amt_ky_truoc'], 2, True)
                    d['divisor_bal_lcl'] = lib.parseFloat(d['divisor_bal_lcl'], 2, True)
                    d['divider_bal_lcl'] = lib.parseFloat(d['divider_bal_lcl'], 2, True)
                    datas.append(d)

            cur.close()
            con.close()
            return self.response_success( datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Chart',
        summary='List',
        tags=["Dashboard"],
        description="""
The `module` has values: 
- **tong_so_but_toan**.
- **thu_phi_dich_vu**.
- **tang_truong_huy_dong**.

The `vung` example: 
- **V02**.

The `kv` example: 
- **K01**.

The `dv` example: 
- **001**.

The `division` example: 
- **A**. khối PFS
- **B**. khối DOANH NGHIỆP

""",
        parameters=[
            OpenApiParameter(
                name="module", type=OpenApiTypes.STR, description="module"
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
                name="division", type=OpenApiTypes.STR, description="division"
            ),
        ],
        # request=ChartRequestSerializer,
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
            key = params['module']
            module = ",P_MODULE=>'{}'".format(key)

            vung = ""
            if 'vung' in params.keys():
                vung = ", P_VUNG=>'{}'".format(params['vung'])

            kv = ""
            if 'kv' in params.keys():
                kv = ", P_KV=>'{}'".format(params['kv'])

            dv = ""
            if 'dv' in params.keys():
                dv = ", P_DV=>'{}'".format(params['dv'])

            division = ""
            if 'division' in params.keys():
                division = ", P_DIVISION=>'{}'".format(params['division'])

            # page_number = 1
            # if 'page_number' in params.keys():
            #     page_number = int(params['page_number'])
            # call the function
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_CHART( P_MAN_HINH=>'TRANG_CHU'{}{}{}{}{} ) FROM DUAL".format(module, vung, kv, dv, division)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                if data_cursor is not None:

                    if key == 'tong_so_but_toan' or key == 'thu_phi_dich_vu':
                        total = 0
                        dd = {}
                        for data in data_cursor:
                            print(data)
                            # dd.append(data)
                            ids = lib.create_key(data[1])
                            title = lib.parseString(data[3])
                            val = lib.parseFloat(data[2])
                            unit = lib.parseString(data[4])

                            if ids not in dd:
                                dd[ids] = {
                                    'id': ids,
                                    'title': title,
                                    'val': val,
                                    'unit': unit,
                                }
                            else:
                                d = dd[ids]
                                d['val'] = d['val'] + val

                            if unit == '%':
                                total = total + val

                        tt = 100
                        valmax = None

                        for key in dd:
                            d = dd[key]

                            # ids = lib.create_key(data[1])
                            # title = lib.parseString(data[3])
                            val = d['val']
                            unit = d['unit']

                            if total == 0:
                                val = 0
                            elif unit == '%':
                                val = round(val / total * 100, 2)
                                tt = tt - val
                                d['val'] = val
                            else:
                                d['val'] = round(val)

                            if unit == '%':
                                if valmax is None:
                                    valmax = d
                                elif valmax['val'] < val:
                                    valmax = d

                            datas.append(d)

                        if valmax is not None:
                            print(valmax)
                            valmax['val'] = valmax['val'] + round(tt,2)
                    else:
                        for data in data_cursor:
                            # print(data)
                            val = {
                                'id': lib.create_key(data[1]),
                                'title': lib.parseString(data[3]),
                                'val': lib.parseFloat(data[2]),
                                'unit': lib.parseString(data[4])
                            }
                            datas.append(val)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

