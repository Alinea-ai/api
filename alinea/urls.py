from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from alinea_api.views.access_request_item import set_access_request_item_status, \
    get_access_request_items
from alinea_api.views.test import websocket_test, access_requests_view

schema_view = get_schema_view(
   openapi.Info(
      title="Alinea API",
      default_version='v1',
      description="API documentation for Alinea",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('alinea_api.urls')),
    path('singularity/', include('singularity.urls')),
    path('websocket-test/', websocket_test, name='websocket_test'),
    path('user_websocket_test/', access_requests_view, name='user_websocket_test' ),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
