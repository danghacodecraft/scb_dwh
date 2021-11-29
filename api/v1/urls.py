from django.urls import include, path

urlpatterns = [
    path('users/', include('api.v1.user.urls')),
    path('dashboard/', include('api.v1.dashboard.urls')),
    path('organization/', include('api.v1.organization.urls')),
    path('gis/', include('api.v1.gis.urls')),
    path('report/', include('api.v1.report.urls')),
]
