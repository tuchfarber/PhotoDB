from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='PhotoDB API')

urlpatterns = [
    path('api/v1/', include('photodb.apps.api.urls')),
    path('api-docs/', schema_view),
    path('api_auth/', include('rest_framework.urls')),
    path('', include('photodb.apps.photodb.urls')),
    path('rest-auth/', include('rest_auth.urls'))
]
