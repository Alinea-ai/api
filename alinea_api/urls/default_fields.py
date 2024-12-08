from django.urls import path
from alinea_api.views.default_fields import DefaultFieldListCreateView, DefaultFieldDetailView, \
    DefaultFieldGroupedByTypeView

urlpatterns = [
    path('', DefaultFieldListCreateView.as_view(), name='defaultfield_list_create'),
    path('<int:pk>/', DefaultFieldDetailView.as_view(), name='defaultfield_detail'),
    path('grouped_by_type/', DefaultFieldGroupedByTypeView.as_view(), name='defaultfield_grouped_by_type'),
]

