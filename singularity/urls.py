from django.urls import path

from singularity.views.user import user_summary

urlpatterns = [
    path('user/summary', user_summary, name='user_summary'),
    path('user/query', user_summary, name='user_query'),
]