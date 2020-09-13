from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Activation(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    key = models.CharField(
        max_length=32,
    )
    created = models.DateTimeField(
        auto_now=True,
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


class EmailTemplates(models.Model):
    created = models.DateTimeField(
        auto_now=True,
    )
    template = models.FilePathField()

    class Meta:
        db_table = 'email_templates'


class User(AbstractUser):
    pass

    class Meta:
        db_table = 'auth_user'
