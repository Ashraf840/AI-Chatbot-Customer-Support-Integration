from django.apps import AppConfig


class AuthenticationappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authenticationApp"

    # initialize the django-signals
    def ready(self):
        import authenticationApp.signals
