from django.urls import path

from singularity.views.campaigns import prospects

urlpatterns = [
    path('campaign/prospects', prospects, name='campaigns'),
]