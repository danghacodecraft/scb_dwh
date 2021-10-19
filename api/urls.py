from django.conf.urls import include
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)

from config.root_local import REDOC_SUB_ENDPOINT, SWAGGER_SUB_ENDPOINT
from config.settings import DEBUG

urlpatterns = [
    path('v1/', include('api.v1.urls')),
]

if DEBUG:
    # API DOCUMENT URLS
    # --------------------------------------------------------------------------------------------------
    # Urls listed in api_url_patterns will appear on schema.

    api_url_v1_patterns = [
        path('api/v1/', include("api.v1.urls")),
    ]

    urlpatterns += [
        path('v1/schema/', SpectacularAPIView.as_view(urlconf=api_url_v1_patterns, api_version='v1'), name="schema_v1"),
        path('v1/' + SWAGGER_SUB_ENDPOINT, SpectacularSwaggerView.as_view(url_name="schema_v1"), name='swagger_v1'),
        path('v1/' + REDOC_SUB_ENDPOINT, SpectacularRedocView.as_view(url_name="schema_v1"), name='redoc_v1')
    ]
