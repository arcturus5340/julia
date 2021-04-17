from django.db import models
from django.conf import settings
from jsonfield import JSONField
from unixtimestampfield.fields import UnixTimeStampField
from django.contrib.auth.models import User
import itertools
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from datetime import datetime


class Contest(models.Model):
    title = models.CharField(
        max_length=128,
        unique=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(64)],
    )
    description = models.TextField(
        unique=True,
    )
    start_time = UnixTimeStampField(default=datetime.now)
    duration = models.DurationField(default=timezone.timedelta(hours=2))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = 'contest'


class Task(models.Model):
    title = models.CharField(
        max_length=64,
        unique=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(64)],
    )
    content = models.TextField(
        unique=True,
    )
    contest = models.ForeignKey(
        Contest,
        on_delete=models.PROTECT,
        related_name='tasks',
    )
    ml = models.IntegerField(
        default=268435456,
    )
    tl = models.IntegerField(
        default=2,
    )
    _order = models.IntegerField()

    def get_samples(self):
        try:
            test_cases = itertools.islice(TestCase.objects.filter(task=self).values_list('input', 'output'), 2)
        except ValueError:
            test_cases = []
        return list(test_cases)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        unique_together = ('contest', '_order')
        ordering = ('_order', )


class TestCase(models.Model):
    input = models.TextField()
    output = models.TextField()
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.input}"

    class Meta:
        db_table = 'contest_test_case'
        unique_together = ('input', 'output', 'task')


class Solution(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=2,
    )
    dispatch_time = models.DateTimeField(
        auto_now_add=True
    )
    details = JSONField()
    lang = models.TextField()
    code = models.FilePathField(
        path=settings.CODE_URL,
    )


class Result(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
    )
    attempts = JSONField()
    decision_time = JSONField()

    class Meta:
        unique_together = ('user', 'contest')
