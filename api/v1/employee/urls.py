from django.urls import path

from api.v1.employee.views import EmployeeView

urlpatterns = [
    path('emp_list/', EmployeeView.as_view({'get': 'emp_list'})),
    path('emp_detail/', EmployeeView.as_view({'get': 'emp_detail'})),
    path('dep_list/', EmployeeView.as_view({'get': 'dep_list'})),

    path('brn_detail/', EmployeeView.as_view({'get': 'brn_detail'})),
]
