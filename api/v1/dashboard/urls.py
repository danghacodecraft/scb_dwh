from django.urls import path

from api.v1.dashboard.views import DashboardView

urlpatterns = [
    path('data/', DashboardView.as_view({'get': 'data'})),
    path('chart/', DashboardView.as_view({'post': 'chart'}))
]
