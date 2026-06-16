from django.apps import AppConfig

class NoticiasAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'noticias_app'

    def ready(self):
        import noticias_app.signals
