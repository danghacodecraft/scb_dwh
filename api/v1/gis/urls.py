from django.urls import path

from api.v1.gis.views import GisView

urlpatterns = [
    path('region/', GisView.as_view({'get': 'region'})),
    path('branch/', GisView.as_view({'get': 'branch'})),
    path('search/', GisView.as_view({'get': 'search'}))

]
