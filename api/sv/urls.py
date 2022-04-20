from django.urls import include, path

urlpatterns = [
    path('v1/employee/', include('api.sv.employee.urls')),
]
