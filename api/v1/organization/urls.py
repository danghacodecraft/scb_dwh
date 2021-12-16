from django.urls import path

from api.v1.organization.views import OrganizationView

urlpatterns = [
    path('data/', OrganizationView.as_view({'get': 'data'})),

    path('region/', OrganizationView.as_view({'get': 'region'})),
    path('region_list/', OrganizationView.as_view({'get': 'region_list'})),

    path('branch/', OrganizationView.as_view({'get': 'branch'})),
    path('branch_list/', OrganizationView.as_view({'get': 'branch_list'})),


    path('home/', OrganizationView.as_view({'get': 'home'})),
    path('emp_info/', OrganizationView.as_view({'get': 'emp_info'})),

]
