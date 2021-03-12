from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


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

    class Meta:
        db_table = 'auth_activation'


class EmailTemplates(models.Model):
    created = models.DateTimeField(
        auto_now=True,
    )
    template = models.FilePathField()

    class Meta:
        db_table = 'email_templates'


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(), MinLengthValidator(3), MaxLengthValidator(32)],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )

    class Meta:
        db_table = 'auth_user'
