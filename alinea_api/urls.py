from django.urls import path, include
from rest_framework import routers
from .views import (
    EntityViewSet,
    AccessRequestViewSet,
    AccessRequestItemViewSet,
)

router = routers.DefaultRouter()
router.register(r'entities', EntityViewSet)
router.register(r'access-requests', AccessRequestViewSet)
router.register(r'access-request-items', AccessRequestItemViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]
