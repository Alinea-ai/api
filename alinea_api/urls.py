# alinea_api/urls.py

from django.urls import path, include
from rest_framework import routers

from .views.access_request import AccessRequestViewSet
from .views.access_request_item import AccessRequestItemViewSet, set_access_request_item_status, \
    get_access_request_items
from .views.document import get_documents, add_document, update_document, delete_document, \
    get_documents_by_request_id
from .views.entity import EntityViewSet
from .views.template import create_template, get_templates_by_entity
from .views.user import search_users

router = routers.DefaultRouter()
router.register(r'entities', EntityViewSet)
router.register(r'access-requests', AccessRequestViewSet)
router.register(r'access-request-items', AccessRequestItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('set_access_request_item_status/', set_access_request_item_status, name='set_access_request_item_status'),
    path('access_request_items/', get_access_request_items, name='get_access_request_items'),
    # path('<access_request_id>/documents/', get_documents, name='get_access_request_items'),

    path('search/users/', search_users, name='search_users'),

    path('access_request_itme/status/', set_access_request_item_status, name='approve_access_request_item'),
    path('access_request_items/', get_access_request_items, name='get_access_request_items'),
    path('access_request/<access_request_id>/documents/', get_documents_by_request_id, name='get_access_request_items'),

    path('template/create/', create_template, name='create_template'),
    path('template/', get_templates_by_entity, name='get_templates_by_entity'),

    path('users/<user_id>/documents/', get_documents, name='get_documents'),
    path('users/<user_id>/documents/<document_type>/add', add_document, name='add_document'),
    path('users/<user_id>/documents/<document_type>/update', update_document, name='update_document'),
    path('users/<user_id>/documents/<document_type>/delete', delete_document, name='delete_document'),

]
