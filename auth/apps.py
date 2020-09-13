from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'auth'
    label = 'custom_auth'

    def ready(self):
        from auth import scheduled_tasks
        scheduled_tasks.start()