from django.urls import include, path

from api.v1.report.business_unit.views import BusinessUnitView

urlpatterns = [
    path('data/', BusinessUnitView.as_view({'get': 'data'})),
    path('chart/', BusinessUnitView.as_view({'post': 'chart'})),

    path('detail/', include('api.v1.report.business_unit.detail.urls'))
]
