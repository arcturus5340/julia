from django.db import models
from django.contrib.auth.models import User


class Code(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    file = models.FileField()


class Task(models.Model):
    title = models.CharField(
        max_length=64
    )
    content = models.TextField()


class TestCase(models.Model):
    input = models.TextField()
    output = models.TextField()
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'test_case'
