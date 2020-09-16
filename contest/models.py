from django.db import models
from django.conf import settings
from jsonfield import JSONField
from unixtimestampfield.fields import UnixTimeStampField
from django.contrib.auth.models import User
import itertools
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Contest(models.Model):
    title = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(3)],
    )
    description = models.TextField()
    start_time = UnixTimeStampField(auto_now=True)
    duration = models.DurationField(default=timezone.timedelta(hours=2))

    class Meta:
        db_table = 'contest'


class Task(models.Model):
    title = models.CharField(
        max_length=64,
        validators=[MinLengthValidator(3)],
    )
    content = models.TextField()
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
            input, output = zip(*test_cases)
        except ValueError:
            input, output = [], []
        return {
            'input': input,
            'output': output,
        }

    class Meta:
        unique_together = ('contest', '_order')


class TestCase(models.Model):
    input = models.TextField()
    output = models.TextField()
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'contest_test_case'


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
