from django.urls import path

from ..views.user import search_users

urlpatterns = [
    path('users/', search_users, name='search_users'),

]
