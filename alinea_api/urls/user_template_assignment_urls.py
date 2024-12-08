from django.urls import path
from ..views.user_template_assignment import UserTemplateAssignmentListCreateView, \
    UserTemplateAssignmentDetailView, UserSpecificTemplateAssignmentListView

urlpatterns = [
    path('', UserTemplateAssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('<int:pk>/', UserTemplateAssignmentDetailView.as_view(), name='assignment-detail'),
    path('my-assignments/', UserSpecificTemplateAssignmentListView.as_view(), name='my-assignments'),
]