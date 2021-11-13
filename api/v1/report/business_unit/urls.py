from django.urls import path

from api.v1.report.business_unit.views import BusinessUnitView

urlpatterns = [
    path('data/', BusinessUnitView.as_view({'get': 'data'})),
    path('chart/', BusinessUnitView.as_view({'post': 'chart'}))


]
