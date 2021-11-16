from django.urls import path

from api.v1.report.business_unit.detail.views import BusinessDetailUnitView

urlpatterns = [
    path('data/', BusinessDetailUnitView.as_view({'get': 'data'})),
    path('chart/', BusinessDetailUnitView.as_view({'post': 'chart'}))


]
