from django.db import models
from django.contrib.auth.models import User

class ActivationKeys(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    key = models.CharField(
        max_length=32,
    )
    is_password_reset = models.BooleanField(
        default=False,
    )
    is_email_verification = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = 'auth_activation_keys'
