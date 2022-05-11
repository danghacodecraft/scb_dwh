from django.urls import path

from api.sv.dashboard.views import DashboardSVView


urlpatterns = [
    path('data/', DashboardSVView.as_view({'get': 'data'})),
    path('dataex/', DashboardSVView.as_view({'get': 'dataex'})),
    path('chart/', DashboardSVView.as_view({'get': 'chart'})),

]
