from django.apps import AppConfig


class AluminiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alumini'
    
    def ready(self):
        import alumini.signals  
