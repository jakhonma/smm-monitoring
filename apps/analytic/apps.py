from django.apps import AppConfig


class AnalyticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analytic'
    
    def ready(self):
        import apps.analytic.signals  # noqa
