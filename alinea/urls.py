from django.contrib import admin
from django.urls import path, include
from alinea_api.views import websocket_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('alinea_api.urls')),
    path('websocket-test/', websocket_test, name='websocket_test'),
]
