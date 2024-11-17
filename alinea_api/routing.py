from django.urls import re_path

from alinea_api.consumers.dashboard_consumer import NotificationConsumer
from alinea_api.consumers.user_consumer import UserNotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/concent/$', NotificationConsumer.as_asgi()),
    re_path(r'^ws/user_concent/$', UserNotificationConsumer.as_asgi())
]