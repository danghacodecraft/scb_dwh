from django.urls import include, path

from config.settings import DEBUG
from .views import get_otp_server, get_health

urlpatterns = [
    path('users/', include('api.v1.user.urls')),
    path('dashboard/', include('api.v1.dashboard.urls')),
    path('employee/', include('api.v1.employee.urls')),
    path('organization/', include('api.v1.organization.urls')),
    path('gis/', include('api.v1.gis.urls')),
    path('report/', include('api.v1.report.urls')),
]

if DEBUG:
    urlpatterns += [
        path('get-otp/', get_otp_server),
        path('check-health/', get_health),
    ]
