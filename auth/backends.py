from django.contrib.auth.backends import ModelBackend


class VerificationBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return user.groups.filter(name='Verified Users').exists() and super().user_can_authenticate(user)
