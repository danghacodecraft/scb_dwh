from django.urls import path

from api.v1.dashboard.views import DashboardView

urlpatterns = [
    path('data/', DashboardView.as_view({'get': 'data'})),
    path('dataex/', DashboardView.as_view({'get': 'dataex'})),
    path('chart/', DashboardView.as_view({'get': 'chart'})),

]
