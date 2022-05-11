from django.urls import include, path

urlpatterns = [
    path('v1/employee/', include('api.sv.employee.urls')),
    path('v1/gis/', include('api.sv.gis.urls')),
    path('v1/dashboard/', include('api.sv.dashboard.urls')),
]
