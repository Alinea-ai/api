from django.urls import path, include
from rest_framework.routers import DefaultRouter

from alinea_api.views.visit import VisitsViewSet

router = DefaultRouter()
router.register( '', VisitsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]