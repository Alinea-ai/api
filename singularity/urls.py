# your_app/urls.py

from django.urls import path

from singularity.views.user import UserSummaryView, UserQueryView

urlpatterns = [
    path('user/summary/', UserSummaryView.as_view(), name='user_summary'),
    path('user/query/', UserQueryView.as_view(), name='user_query'),  # Corrected to UserQueryView
]
