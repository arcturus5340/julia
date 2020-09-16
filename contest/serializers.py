from rest_framework import serializers
from contest.models import Contest, Task, Solution, Result, TestCase
from django.conf import settings
import time
import datetime
from django.utils import datetime_safe

class TimestampDurationInSecondsField(serializers.DurationField):
    def to_native(self, value):
        return value*1000

    def to_representation(self, value):
        return int(value.total_seconds())

class TimestampDateTimeField(serializers.IntegerField):
    def to_native(self, value):
        return datetime.datetime.fromtimestamp(value)

    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))


class TestCaseSerializer(serializers.ModelSerializer):
    input = serializers.CharField()
    output = serializers.CharField()

    class Meta:
        model = TestCase
        fields = ['input', 'output']


class TaskSerializer(serializers.ModelSerializer):
    contest = serializers.PrimaryKeyRelatedField(
        queryset=Contest.objects.all(),
    )
    test_cases = serializers.ListField(
        child=TestCaseSerializer(),
        read_only=True,
    )

    class Meta:
        model = Task
        fields  = ['id', 'title', 'content', 'contest', 'tl', 'ml', 'samples', 'test_cases', '_order']
        read_only_fields = ['id', 'samples']
        extra_kwargs = {
            'samples': {'source': 'get_samples'},
            'title': {'required': True},
            'content': {'required': True},
            'contest': {'required': True},
            '_order': {'write_only': True},
        }


class ContestSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False,
    )
    start_time = TimestampDateTimeField(
        required=False,
    )
    duration = TimestampDurationInSecondsField(
        required=False,
    )

    class Meta:
        model = Contest
        fields = ['id', 'title', 'description', 'tasks', 'start_time', 'duration']
        read_only_fields = ['id', 'tasks']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
        }

class SolutionSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    task = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    dispatch_time = TimestampDateTimeField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = Solution
        fields = read_only_fields = ['id', 'author', 'task', 'status', 'dispatch_time']
        extra_kwargs = {
            'status': {'required': False},
        }


class SolutionDetailSerializer(SolutionSerializer):
    details = serializers.DictField(
        required=False,
    )
    code = serializers.SerializerMethodField('get_code_url')

    def get_code_url(self, obj):
        return f'http://{self.context["request"].get_host()}/{settings.CODE_DIR}{obj.code.split("/")[-1]}'

    class Meta(SolutionSerializer.Meta):
        fields = SolutionSerializer.Meta.fields.copy()
        fields.extend(['details', 'lang', 'code'])


class ResultSerializer(serializers.ModelSerializer):
    attempts = serializers.ListField()
    decision_time = serializers.ListField()

    class Meta:
        model = Result
        fields = ['user', 'attempts', 'decision_time']
