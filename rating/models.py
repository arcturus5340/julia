from django.db import models
from django.contrib.auth.models import User


class History(models.Model):
    date = models.DateTimeField(
        auto_now_add=True,
    )
    rating = models.IntegerField(
        default=1024,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
