from django.urls import path

from api.v1.employee.views import EmployeeView

urlpatterns = [
    path('emp_list/', EmployeeView.as_view({'get': 'emp_list'})),
    path('emp_detail/', EmployeeView.as_view({'get': 'emp_detail'})),
    path('emp_detail_kpi/', EmployeeView.as_view({'get': 'emp_detail_kpi'})),
    path('emp_detail_profile/', EmployeeView.as_view({'get': 'emp_detail_profile'})),

    path('dep_list/', EmployeeView.as_view({'get': 'dep_list'})),
]
