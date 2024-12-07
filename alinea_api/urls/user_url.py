# your_app/urls.py

from django.urls import path
from ..views.document import DocumentListView, DocumentDetailView, DocumentByRequestIDView

urlpatterns = [

    path('<int:user_id>/documents/', DocumentListView.as_view(), name='document_list'),
    path('<int:user_id>/documents/<str:document_type>/', DocumentDetailView.as_view(), name='document_detail'),
    path('access-requests/<int:access_request_id>/documents/', DocumentByRequestIDView.as_view(), name='documents_by_request_id'),
]

