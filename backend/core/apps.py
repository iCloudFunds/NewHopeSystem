from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Name must match the full directory path
    name = 'backend.core'
    # Label is how Django refers to it in settings and models
    label = 'core'