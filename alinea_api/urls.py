# alinea_api/urls.py

from django.urls import path, include
from rest_framework import routers

from .views.access_request import AccessRequestViewSet
from .views.access_request_item import AccessRequestItemViewSet, set_access_request_item_status, \
    get_access_request_items
from .views.document import get_documents
from .views.entity import EntityViewSet
from .views.user import search_users

router = routers.DefaultRouter()
router.register(r'entities', EntityViewSet)
router.register(r'access-requests', AccessRequestViewSet)
router.register(r'access-request-items', AccessRequestItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('set_access_request_item_status/', set_access_request_item_status, name='set_access_request_item_status'),
    path('access_request_items/', get_access_request_items, name='get_access_request_items'),
    path('<access_request_id>/documents/', get_documents, name='get_access_request_items'),
    path('search-users/', search_users, name='search_users')
]
