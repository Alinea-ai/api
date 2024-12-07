from django.urls import path, include
from rest_framework import routers

from ..views.entity import EntityViewSet

router = routers.DefaultRouter()
router.register(r'entity', EntityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
