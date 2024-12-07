from django.urls import path

from alinea_api.views.template import TemplateView

urlpatterns = [
    path('templates/', TemplateView.as_view(), name='templates'),
]
