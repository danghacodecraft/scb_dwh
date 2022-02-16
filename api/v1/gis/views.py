import cx_Oracle
from drf_spectacular.types import OpenApiTypes

import api.v1.function as lib

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.gis.serializers import BranchResponseSerializer, RegionResponseSerializer, AreaResponseSerializer, BranchAreaResponseSerializer

def myRegion(e):
    return e['region_id']

def myBranch(e):
    return e['branch_id']

def myArea(e):
    return e['NAME']

def filterName(name_lower):
    if "kênh" in name_lower or "khác" in name_lower or "hội sở" in name_lower:
        return True
    return False

LATITUDE_DEFAULT = 10.771912559303502
LONGITUDE_DEFAULT = 106.70564814326777
TYPE_DEFAULT = "CN Đa năng"

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
                userid = "P_USER_ID=>'{}'".format(params['userid'].upper())

            # ======================================================================
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_LOCATION({}) FROM DUAL".format(userid)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            gis = {
                'ALL': {
                    'region_id': 'ALL',
                    'region_name': 'Tất cả',
                    'branches': {
                        'ALL': {
                            'branch_id': 'ALL',
                            'branch_name': 'Tất cả',
                            'longitude': LONGITUDE_DEFAULT,
                            'latitude': LATITUDE_DEFAULT,
                            'type': TYPE_DEFAULT
                        }
                    }
                }
            }
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    print(data)
                    region_id = data[0].strip()
                    region_name = data[1].strip()
                    branch_id = data[6].strip()
                    branch_name = data[7].strip()
                    latitude = data[8] if data[8] is not None else LATITUDE_DEFAULT
                    longitude = data[9] if data[9] is not None else LONGITUDE_DEFAULT
                    branchtype = data[10]
                    # ('V98', 'KÊNH KINH DOANH TRỰC TIẾP MIỀN NAM', 'K99', 'KHÁC', 'C07', 'Cống Quỳnh', '246', 'HUB AUTO - HCM 1', None, None)

                    if filterName(region_name.lower()):
                        continue

                    if region_name not in gis:
                        gis[region_name] = {
                            'region_id': region_id,
                            'region_name': region_name,
                            'branches': {
                                'ALL': {
                                    'branch_id': 'ALL',
                                    'branch_name': 'Tất cả',
                                    'longitude': LONGITUDE_DEFAULT,
                                    'latitude': LATITUDE_DEFAULT,
                                    'type': TYPE_DEFAULT
                                }
                            }
                        }

                    region = gis[region_name]
                    if branch_name not in region['branches']:
                        region['branches'][branch_name] = {
                            'branch_id': branch_id,
                            'branch_name': branch_name,
                            'longitude': longitude,
                            'latitude': latitude,
                            'type': branchtype
                        }

                        gis['ALL']['branches'][branch_name] = {
                            'branch_id': branch_id,
                            'branch_name': branch_name,
                            'longitude': longitude,
                            'latitude': latitude,
                            'type': branchtype
                        }

            print("||||||||||||||||||||||||||||||||||")
            datas = []
            for region_name in sorted(gis.keys()):
                print("======================================")
                print(region_name)
                print("-----------------------------")
                region = gis[region_name]
                branches = []
                left = 120
                right = 100
                top = 10
                bottom = 20

                for branch_name in sorted(region['branches'].keys()):
                    print(branch_name)
                    branch = region['branches'][branch_name]
                    branch_id = branch['branch_id']
                    branch_name = branch['branch_name']
                    longitude = branch['longitude']
                    latitude = branch['latitude']
                    branches.append({
                        'branch_id': branch_id,
                        'branch_name': branch_name,
                        'longitude': longitude,
                        'latitude': latitude,
                        'type': branch['type']
                    })

                    if branch_id != 'ALL':
                        left = left if left < longitude else longitude
                        right = right if right > longitude else longitude
                        top = top if top > latitude else latitude
                        bottom = bottom if bottom < latitude else latitude

                if region_id == 'ALL':
                    left = 100
                    right = 120
                    top = 20
                    bottom = 10

                datas.append({
                    'region_id': region['region_id'],
                    'region_name': region['region_name'],
                    'branches': branches,
                    'left': left,
                    'right': right,
                    'top': top,
                    'bottom': bottom
                })
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
                userid = "P_USER_ID=>'{}'".format(params['userid'].upper())

            # ======================================================================
            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_LOCATION({}) FROM DUAL".format(userid)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            gis = {
                'ALL': {
                    'area_id': 'ALL',
                    'area_name': 'Tất cả',
                    'branches': {
                        'ALL': {
                            'branch_id': 'ALL',
                            'branch_name': 'Tất cả',
                            'longitude': LONGITUDE_DEFAULT,
                            'latitude': LATITUDE_DEFAULT,
                            'type': TYPE_DEFAULT
                        }
                    }
                }
            }
            if len(res) > 0:
                data_cursor = res[0]
                for data in data_cursor:
                    # print(data)
                    area_id = data[2].strip()
                    area_name = data[3].strip()
                    branch_id = data[6].strip()
                    branch_name = data[7].strip()
                    latitude = data[8] if data[8] is not None else LATITUDE_DEFAULT
                    longitude = data[9] if data[9] is not None else LONGITUDE_DEFAULT
                    branchtype = data[10]

                    if filterName(area_name.lower()):
                        continue

                    # ('V98', 'KÊNH KINH DOANH TRỰC TIẾP MIỀN NAM', 'K99', 'KHÁC', 'C07', 'Cống Quỳnh', '246', 'HUB AUTO - HCM 1', None, None)
                    if area_id not in gis:
                        gis[area_id] = {
                            'area_id': area_id,
                            'area_name': area_name,
                            'branches': {
                                'ALL': {
                                    'branch_id': 'ALL',
                                    'branch_name': 'Tất cả',
                                    'longitude': LONGITUDE_DEFAULT,
                                    'latitude': LATITUDE_DEFAULT,
                                    'type': TYPE_DEFAULT
                                }
                            }
                        }

                    area = gis[area_id]
                    if branch_name not in area['branches']:
                        area['branches'][branch_name] = {
                            'branch_id': branch_id,
                            'branch_name': branch_name,
                            'longitude': longitude,
                            'latitude': latitude,
                            'type': branchtype
                        }

                        gis['ALL']['branches'][branch_name] = {
                            'branch_id': branch_id,
                            'branch_name': branch_name,
                            'longitude': longitude,
                            'latitude': latitude,
                            'type': branchtype
                        }

            datas = []
            for area_name in sorted(gis):
                area = gis[area_name]
                branches = []
                left = 120
                right = 100
                top = 10
                bottom = 20

                for branch_name in sorted(area['branches']):
                    branch = area['branches'][branch_name]
                    branch_id = branch['branch_id']
                    branch_name = branch['branch_name']
                    longitude = branch['longitude']
                    latitude = branch['latitude']
                    branches.append({
                        'branch_id': branch_id,
                        'branch_name': branch_name,
                        'longitude': longitude,
                        'latitude': latitude,
                        'type': branch['type']
                    })
                    if branch_id != 'ALL':
                        left = left if left < longitude else longitude
                        right = right if right > longitude else longitude
                        top = top if top > latitude else latitude
                        bottom = bottom if bottom < latitude else latitude

                area_id = area['area_id']
                area_name = area['area_name']
                if area_id == 'ALL':
                    left = 100
                    right = 120
                    top = 20
                    bottom = 10

                str = "{}:{}: {}, {}, {}, {}".format(area_id, area_name, left, right, top, bottom)
                print(str)

                datas.append({
                    'ID': area_id,
                    'NAME': area_name,
                    'branches': branches,
                    'left': left,
                    'right': right,
                    'top': top,
                    'bottom': bottom
                })
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
            con, cur = lib.connect()
            params = request.query_params.dict()

            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'].upper())

            region = ""
            if 'region' in params.keys():
                region = ", P_VUNG=>'{}'".format(params['region'])

            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_LOCATION({}{}) FROM DUAL".format(userid, region)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            datas = []
            if len(res) > 0:
                data_cursor = res[0]
                gis = {}
                for data in data_cursor:
                    print(data)
                    #('V98', 'KÊNH KINH DOANH TRỰC TIẾP MIỀN NAM', 'K99', 'KHÁC', 'C07', 'Cống Quỳnh', '246', 'HUB AUTO - HCM 1', None, None)
                    branch_id = data[6].strip()
                    if branch_id not in gis.keys() and data[8] != None and data[9] != None:
                        gis[branch_id] = data
                        val = {
                            'region_id': data[0].strip(),
                            'region_name': data[1].strip(),
                            'area_id': data[2].strip(),
                            'area_name': data[3].strip(),
                            'branch_id': branch_id,
                            'branch_name': data[7].strip(),
                            'latitude': data[8],
                            'longitude': data[9],
                            'type': data[10].strip()
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
        operation_id='Branch GeoJson',
        summary='List',
        tags=["GIS"],
        description="Branch GeoJson",
        parameters=[
            OpenApiParameter(
                name="userid", type=OpenApiTypes.STR, description="userid"
            ),
            OpenApiParameter(
                name="vung", type=OpenApiTypes.STR, description="vung"
            ),
            OpenApiParameter(
                name="kv", type=OpenApiTypes.STR, description="kv"
            )
        ],
        # request=BranchRequestSerializer,
        responses={
            status.HTTP_201_CREATED: BranchResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def branchgeojson(self, request):
        try:
            con, cur = lib.connect()
            params = request.query_params.dict()

            userid = "P_USER_ID=>'THANGHD'"
            if 'userid' in params.keys():
                userid = "P_USER_ID=>'{}'".format(params['userid'].upper())

            sql = "SELECT obi.CRM_DWH_PKG.FUN_GET_LOCATION({}) FROM DUAL".format(userid)
            print(sql)
            cur.execute(sql)
            res = cur.fetchone()

            TYPES = {
                "CN Cấp 1": "CNC1",
                "CN Cấp 2": "CNC2",
                "Siêu CN Cấp 1": "SCNC1",
                "Siêu CN Cấp 2": "SCNC2",
                "CN Đa năng": "CNDN",
                "CN Chuẩn": "CNC",
                "KXD": "CNDN"
            }
            features = []
            if len(res) > 0:
                data_cursor = res[0]
                gis = {}
                for data in data_cursor:
                    print(data)
                    # ('V98', 'KÊNH KINH DOANH TRỰC TIẾP MIỀN NAM', 'K99', 'KHÁC', 'C07', 'Cống Quỳnh', '246', 'HUB AUTO - HCM 1', None, None)
                    branch_id = data[6].strip()
                    if branch_id not in gis.keys() and data[8] != None and data[9] != None:
                        gis[branch_id] = data

                        val = {
                            "id": branch_id,
                            "type": "Feature",
                            "properties": {
                                "id": branch_id,
                                "name": data[7].strip(),
                                "code": branch_id,
                                "address": "",
                                "zone_id": data[0].strip(),
                                "zone_name": data[1].strip(),
                                "area_id": data[2].strip(),
                                "area_name": data[3].strip(),
                                "type": TYPES[data[10].strip()]
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": [data[9], data[8], 0.0]
                            }
                        }

                        # val = {
                        #     'region_id': data[0].strip(),
                        #     'region_name': data[1].strip(),
                        #     'area_id': data[2].strip(),
                        #     'area_name': data[3].strip(),
                        #     'branch_id': branch_id,
                        #     'branch_name': data[7].strip(),
                        #     'latitude': data[8],
                        #     'longitude': data[9],
                        #     'type': data[10].strip()
                        # }
                        features.append(val)

            datas = {
                "type": "FeatureCollection",
                "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                "features": features
            }

            cur.close()
            con.close()
            return self.response_success(datas, status_code=status.HTTP_200_OK)
        except cx_Oracle.Error as error:
            cur.close()
            con.close()
            return self.response_success(error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

