# yourapp/urls.py

from django.urls import path
from ..views.template import TemplateListCreateView, TemplateDetailView

urlpatterns = [
    path('', TemplateListCreateView.as_view(), name='template_list_create'),
    path('<int:id>/', TemplateDetailView.as_view(), name='template_detail'),
]
