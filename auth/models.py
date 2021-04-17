from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _


class Activation(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    key = models.CharField(
        max_length=32,
        unique=True,
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
        max_length=32,
        unique=True,
        help_text=_('Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[ASCIIUsernameValidator(), MinLengthValidator(3), MaxLengthValidator(32)],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        unique=True,
    )


    def __str__(self):
        return f"{self.username}"

    class Meta:
        db_table = 'auth_user'
