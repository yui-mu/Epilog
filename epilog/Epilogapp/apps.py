from django.apps import AppConfig


class EpilogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Epilogapp'
    
    def ready(self):
        import Epilogapp.templatetags.custom_filters
