from django.urls import include, path

from api.v1.report.all.views import AllView

urlpatterns = [
    #SCREEN C_06
    path('chart/', AllView.as_view({'get': 'chart'})),
    path('chart_pfs/', AllView.as_view({'get': 'chart_pfs'})),
    path('chart_enterprise/', AllView.as_view({'get': 'chart_enterprise'}))
]
