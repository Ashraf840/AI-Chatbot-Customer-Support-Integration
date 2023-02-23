from django.apps import AppConfig


class StaffappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staffApp"

    # initialize the django-signals
    def ready(self):
        import staffApp.signals
