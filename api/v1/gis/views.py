import cx_Oracle
import config.database as db
import json
from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.gis.serializers import BranchRequestSerializer, BranchResponseSerializer, RegionResponseSerializer

def connect():
    # create a connection to the Oracle Database
    con = cx_Oracle.connect(db.DATABASE['USER'], db.DATABASE['PASSWORD'], db.DATABASE['NAME'])
    # create a new cursor
    cur = con.cursor()

    return con, cur

def myRegion(e):
    return e['region_id']

def myBranch(e):
    return e['branch_id']

class GisView(BaseAPIView):
    @extend_schema(
        operation_id='Region',
        summary='List',
        tags=["GIS"],
        description="Region",
        responses={
            status.HTTP_201_CREATED: RegionResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def region(self, request):
        try:
            con, cur = connect()

            sql = 'select obi.CRM_DWH_PKG.FUN_GET_REGION FROM DUAL'

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
        request=BranchRequestSerializer,
        responses={
            status.HTTP_201_CREATED: BranchResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def branch(self, request):
        try:
            serializer = BranchRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            region = serializer.validated_data['region']

            con, cur = connect()
            if region == "":
                sql = "select obi.CRM_DWH_PKG.FUN_GET_LOCATION FROM DUAL"
            else:
                sql = "select obi.CRM_DWH_PKG.FUN_GET_LOCATION(P_VUNG=>'{P_VUNG}') FROM DUAL".format(P_VUNG=region)

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

                    branch_id = data[4].strip()
                    if branch_id not in filter.keys() and data[8] != None and data[9] != None:
                        filter[branch_id] = data
                        val = {
                            'branch_id': branch_id,
                            'branch_name': data[5].strip(),
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