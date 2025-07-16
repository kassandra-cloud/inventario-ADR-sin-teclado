from django.apps import AppConfig


class AdrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adr'

    def ready(self):
        import adr.signals


