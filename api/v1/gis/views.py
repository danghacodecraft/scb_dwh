import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.gis.serializers import BranchResponseSerializer, RegionResponseSerializer, AreaResponseSerializer

def myRegion(e):
    return e['region_id']

def myBranch(e):
    return e['branch_id']

def myArea(e):
    return e['NAME']

class GisView(BaseAPIView):
    @extend_schema(
        operation_id='Region',
        summary='List',
        tags=["GIS"],
        description="Region",
        parameters=[
            OpenApiParameter(
                name="userid", type=OpenApiTypes.STR, description="userid"
            )
        ],
        responses={
            status.HTTP_201_CREATED: RegionResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def region(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()

            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'])

            sql = 'SELECT obi.CRM_DWH_PKG.FUN_GET_REGION({}) FROM DUAL'.format(userid)
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
                        'region_id': data[0].strip(),
                        'region_name': data[1].strip()
                    }
                    datas.append(val)

                datas.sort(key=myRegion)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Branch',
        summary='List',
        tags=["GIS"],
        description="Branch",
        parameters=[
            OpenApiParameter(
                name="userid", type=OpenApiTypes.STR, description="userid"
            ),
            OpenApiParameter(
                name="region", type=OpenApiTypes.STR, description="region"
            )
        ],
        # request=BranchRequestSerializer,
        responses={
            status.HTTP_201_CREATED: BranchResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def branch(self, request):
        try:
            params = request.query_params.dict()

            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'])

            region = ""
            if 'region' in params.keys():
                region = ", P_VUNG=>'{}'".format(params['region'])

            con, cur = lib.connect()
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_LOCATION({}{}) FROM DUAL".format(userid, region)
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

                filter = {}
                for data in data_cursor:
                    print(data)
                    #('V98', 'KÊNH KINH DOANH TRỰC TIẾP MIỀN NAM', 'K99', 'KHÁC', 'C07', 'Cống Quỳnh', '246', 'HUB AUTO - HCM 1', None, None)
                    branch_id = data[6].strip()
                    if branch_id not in filter.keys() and data[8] != None and data[9] != None:
                        filter[branch_id] = data
                        val = {
                            'region_id': data[0],
                            'region_name': data[1],
                            'branch_id': branch_id,
                            'branch_name': data[7].strip(),
                            'latitude': data[8],
                            'longitude': data[9],
                        }
                        datas.append(val)

                datas.sort(key=myBranch)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Search Branch',
        summary='List',
        tags=["GIS"],
        description="Branch",
        parameters=[
            OpenApiParameter(
                name="userid", type=OpenApiTypes.STR, description="userid"
            ),
            OpenApiParameter(
                name="code", type=OpenApiTypes.STR, description="code"
            )
        ],
        # request=BranchRequestSerializer,
        responses={
            status.HTTP_201_CREATED: BranchResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def search(self, request):
        try:
            params = request.query_params.dict()

            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'])

            code = params['code']

            con, cur = lib.connect()
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_LOCATION({}) FROM DUAL".format(userid)
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
                    # ('V98', 'KÊNH KINH DOANH TRỰC TIẾP MIỀN NAM', 'K99', 'KHÁC', 'C07', 'Cống Quỳnh', '246', 'HUB AUTO - HCM 1', None, None)
                    branch_id = data[6].strip()
                    if branch_id == code:
                        val = {
                            'region_id': data[0],
                            'region_name': data[1],
                            'branch_id': branch_id,
                            'branch_name': data[7].strip(),
                            'latitude': data[8],
                            'longitude': data[9],
                        }
                        datas.append(val)
                        break


            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Area',
        summary='List',
        tags=["GIS"],
        description="Area",
        parameters=[
            OpenApiParameter(
                name="userid", type=OpenApiTypes.STR, description="userid"
            ),
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: AreaResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def area(self, request):
        try:
            con, cur = lib.connect()

            params = request.query_params.dict()
            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'])

            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_AREA() from dual".format(userid)
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
                        'ID': data[0],
                        'NAME': data[1]
                    }
                    datas.append(val)
                datas.sort(key=myArea)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id='Area Branch',
        summary='List',
        tags=["GIS"],
        description="""
Param `screen`         
- **K01**.
- **K02**.
""",
        parameters=[
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            ),
        ],
        # request=ChartFRequestSerializer,
        responses={
            status.HTTP_201_CREATED: AreaResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def area_branch(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()

            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'])

            kv = "K01"
            if 'kv' in params.keys():
                kv = params['kv']

            #--------------------------------------------------
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_LOCATION({}) FROM DUAL".format(userid)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            branches = {}
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    # ('V98', 'KÊNH KINH DOANH TRỰC TIẾP MIỀN NAM', 'K99', 'KHÁC', 'C07', 'Cống Quỳnh', '246', 'HUB AUTO - HCM 1', None, None)
                    branch_id = data[6].strip()
                    if branch_id not in branches.keys() and data[8] != None and data[9] != None:
                        branches[branch_id] = {
                            'latitude': data[8],
                            'longitude': data[9],
                        }

            # --------------------------------------------------
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_BRANCH_AREA(P_KV=>'{}') from dual".format( kv)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    branch_id = data[0]
                    val = {
                        'ID': branch_id,
                        'NAME': data[1],
                        'latitude': 0,
                        'longitude': 0,
                        'KHU_VUC': kv
                    }

                    if branch_id in branches.keys():
                        branch = branches[branch_id]
                        val['longitude'] = branch['longitude']
                        val['latitude'] = branch['latitude']

                    datas.append(val)
                datas.sort(key=myArea)

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
