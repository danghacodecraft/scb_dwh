from django.urls import path

from api.sv.gis.views import GISSVView

urlpatterns = [
    path('region/', GISSVView.as_view({'get': 'region'})),
    path('area/', GISSVView.as_view({'get': 'area'})),
    path('branch/', GISSVView.as_view({'get': 'branch'})),
    path('branchgeojson/', GISSVView.as_view({'get': 'branchgeojson'})),
]
