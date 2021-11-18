from django.urls import path

from api.v1.report.business_unit.capital.views import CapitalBusinessView

urlpatterns = [
    path('data/', CapitalBusinessView.as_view({'get': 'data'})),
    path('chart/', CapitalBusinessView.as_view({'post': 'chart'}))
]
