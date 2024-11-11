# alinea/asgi.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alinea.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import alinea_api.routing  # Import after Django setup

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            alinea_api.routing.websocket_urlpatterns
        )
    ),
})
