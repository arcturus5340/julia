from django.db import models
from django.contrib.auth.models import User


class Contest(models.Model):
    title = models.CharField(
        max_length=128,
    )
    description = models.TextField()

    class Meta:
        db_table = 'contest'


class Task(models.Model):
    title = models.CharField(
        max_length=64
    )
    content = models.TextField()
    contest = models.ForeignKey(
        Contest,
        on_delete=models.PROTECT,
        related_name='tasks',
    )
    ml = models.IntegerField(
        default=256,
    )
    tl = models.IntegerField(
        default=2,
    )

    def get_samples(self):
        test_cases = TestCase.objects.filter(task=self)[:2]
        return {
            'input': test_cases.values_list('input', flat=True),
            'output': test_cases.values_list('output', flat=True),
        }


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
        User,
        on_delete=models.CASCADE,
    )
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        related_name='solutions',
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        default=None,
    )
    file = models.FileField()
