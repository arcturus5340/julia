from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'auth'
    label = 'custom.auth'

    def ready(self):
        import auth.signals