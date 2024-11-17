from django.contrib import admin
from django.urls import path, include
from alinea_api.views import (
    websocket_test,
    access_requests_view,
    get_access_request_items,
    set_access_request_item_status
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('alinea_api.urls')),
    path('websocket-test/', websocket_test, name='websocket_test'),
    path('user_websocket_test/', access_requests_view, name='user_websocket_test' ),

    path('approve_access_request_item/', set_access_request_item_status, name='approve_access_request_item'),
    path('access_request_items/', get_access_request_items, name='get_access_request_items'),
]
