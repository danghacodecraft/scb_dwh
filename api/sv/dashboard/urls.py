from django.urls import path

from api.sv.dashboard.views import DashboardSVView


urlpatterns = [
    path('data/', DashboardSVView.as_view({'get': 'data'})),
    path('dataex/', DashboardView.as_view({'get': 'dataex'})),
    path('chart/', DashboardView.as_view({'get': 'chart'})),

]
