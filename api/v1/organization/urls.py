from django.urls import path

from api.v1.organization.views import OrganizationView

urlpatterns = [
    path('data/', OrganizationView.as_view({'get': 'data'}))

]
