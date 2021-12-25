from django.urls import include, path

from api.v1.report.all.views import AllView

urlpatterns = [
    #SCREEN C_06
    path('chart/', AllView.as_view({'get': 'chart'})),

]
