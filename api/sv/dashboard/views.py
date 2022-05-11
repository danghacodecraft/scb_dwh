from api.base.base_views import BaseAPIAnonymousView
from api.v1.dashboard.views import DashboardView


class DashboardSVView(BaseAPIAnonymousView):
    data = DashboardView.__dict__['data']
    dataex = DashboardView.__dict__['dataex']
    chart = DashboardView.__dict__['chart']
