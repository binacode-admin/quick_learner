from django.apps import AppConfig


class QuickUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quick_user'

    def ready(self):
        import quick_user.signals
