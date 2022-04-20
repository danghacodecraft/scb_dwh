from django.urls import path

from api.sv.employee.views import EmployeeSVView

urlpatterns = [
    # path('emp_list/', EmployeeSVView.as_view({'get': 'emp_list'})),
    path('emp_detail/', EmployeeSVView.as_view({'get': 'emp_detail'})),
    path('emp_detail_kpi/', EmployeeSVView.as_view({'get': 'emp_detail_kpi'})),
    path('emp_detail_decision/', EmployeeSVView.as_view({'get': 'emp_detail_decision'})),
    path('emp_detail_bonus/', EmployeeSVView.as_view({'get': 'emp_detail_bonus'})),
    path('emp_detail_discipline/', EmployeeSVView.as_view({'get': 'emp_detail_discipline'})),
    path('emp_detail_training/', EmployeeSVView.as_view({'get': 'emp_detail_training'})),
    path('emp_detail_other/', EmployeeSVView.as_view({'get': 'emp_detail_other'})),

    path('emp_detail_work_process/', EmployeeSVView.as_view({'get': 'emp_detail_work_process'})),

    # path('dep_list/', EmployeeView.as_view({'get': 'dep_list'})),
]
