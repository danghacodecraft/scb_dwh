from django.urls import include, path

urlpatterns = [
    path('business_unit/', include('api.v1.report.business_unit.urls')),
    path('enterprise/', include('api.v1.report.enterprise.urls')),
]
