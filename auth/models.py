from django.db import models
from django.contrib.auth.models import User


class Activation(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    key = models.CharField(
        max_length=32,
    )
    is_password_change = models.BooleanField(
        default=False,
    )
    is_email_change = models.BooleanField(
        default=False,
    )
    tmp_data = models.CharField(
        max_length=4096,
        blank=True,
        null=True,
    )
