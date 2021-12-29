from django.urls import path

from api.v1.gis.views import GisView

urlpatterns = [
    path('region/', GisView.as_view({'get': 'region'})),
    path('area/', GisView.as_view({'get': 'area'})),
    path('branch/', GisView.as_view({'get': 'branch'})),

    # path('search/', GisView.as_view({'get': 'search'})),
    # path('area_branch/', GisView.as_view({'get': 'area_branch'})),
]
