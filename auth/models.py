from django.db import models


class ActivationKeys(models.Model):
    key = models.CharField(
        max_length=32,
    )
    is_password_reset = models.BooleanField(
        default=False,
    )
    is_email_verification = models.BooleanField(
        default=False,
    )
