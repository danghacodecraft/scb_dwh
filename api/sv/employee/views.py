from api.base.base_views import BaseAPIAnonymousView
from api.v1.employee.views import EmployeeView


class EmployeeSVView(BaseAPIAnonymousView):
    emp_list = EmployeeView.__dict__['emp_list']
    emp_detail = EmployeeView.__dict__['emp_detail']
    emp_detail_kpi = EmployeeView.__dict__['emp_detail_kpi']
    emp_detail_decision = EmployeeView.__dict__['emp_detail_decision']
    emp_detail_bonus = EmployeeView.__dict__['emp_detail_bonus']
    emp_detail_discipline = EmployeeView.__dict__['emp_detail_discipline']
    emp_detail_training = EmployeeView.__dict__['emp_detail_training']
    emp_detail_other = EmployeeView.__dict__['emp_detail_other']
    emp_detail_work_process = EmployeeView.__dict__['emp_detail_work_process']
