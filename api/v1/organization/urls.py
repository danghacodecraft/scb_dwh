from django.urls import path

from api.v1.organization.views import OrganizationView

urlpatterns = [
    path('data/', OrganizationView.as_view({'get': 'data'})),
    path('region/', OrganizationView.as_view({'get': 'region'})),
    path('branch/', OrganizationView.as_view({'get': 'branch'}))


]
