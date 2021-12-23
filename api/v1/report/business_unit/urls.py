from django.urls import include, path

from api.v1.report.business_unit.views import BusinessUnitView

urlpatterns = [
    path('data/', BusinessUnitView.as_view({'get': 'data'})),
    path('chart/', BusinessUnitView.as_view({'get': 'chart'})),
    path('chart_loan/', BusinessUnitView.as_view({'get': 'chart_loan'})),

    #CUSTOMER
    path('customer/', BusinessUnitView.as_view({'get': 'customer'})),
    path('region/', BusinessUnitView.as_view({'get': 'region'})),
]
