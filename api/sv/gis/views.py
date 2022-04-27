from api.base.base_views import BaseAPIAnonymousView
from api.v1.gis.views import GisView


class GISSVView(BaseAPIAnonymousView):
    region = GisView.__dict__['region']
    area = GisView.__dict__['area']
    branch = GisView.__dict__['branch']
    branchgeojson = GisView.__dict__['branchgeojson']
