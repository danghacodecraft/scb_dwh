from django.urls import include, path

from api.v1.report.enterprise.views import EnterpriseView

urlpatterns = [
    #SCREEN C4
    path('chart_hr/', EnterpriseView.as_view({'get': 'chart_hr'})),
    path('chart_kpi/', EnterpriseView.as_view({'get': 'chart_kpi'})),
    path('chart_income/', EnterpriseView.as_view({'get': 'chart_income'})),
    path('chart_business/', EnterpriseView.as_view({'get': 'chart_business'})),
]
