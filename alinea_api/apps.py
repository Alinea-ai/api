from django.apps import AppConfig


class AlineaApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alinea_api'  # Make sure this matches your app's name

    def ready(self):
        # Import signal handlers
        from . import signals