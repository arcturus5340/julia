from rest_framework import serializers
from contest.models import Contest, Task, Solution, Result
from django.conf import settings
from rest_framework.reverse import reverse

class TaskSerializer(serializers.ModelSerializer):
    contest = serializers.PrimaryKeyRelatedField(
        queryset=Contest.objects.all(),
    )

    class Meta:
        model = Task
        fields  = ['id', 'title', 'content', 'contest', 'tl', 'ml', 'samples', '_order']
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
    )

    class Meta:
        model = Contest
        fields = ['id', 'title', 'description', 'tasks', 'start_time', 'duration']
        read_only_fields = ['id']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'tasks': {'required': True},
        }


class SolutionSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    task = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    class Meta:
        model = Solution
        fields = read_only_fields = ['id', 'author', 'task', 'status', 'dispatch_time']
        extra_kwargs = {
            'status': {'required': False},
        }

class SolutionDetailSerializer(serializers.ModelSerializer):
    details = serializers.DictField(
        required=False,
    )
    file = serializers.SerializerMethodField('get_file_url', required=False)

    def get_file_url(self, obj):
        return f'http://{self.context["request"].get_host()}/{settings.CODE_DIR}{obj.code.split("/")[-1]}'

    class Meta(SolutionSerializer.Meta):
        fields = SolutionSerializer.Meta.fields.copy()
        fields.extend(['details', 'lang', 'file'])


class ResultSerializer(serializers.ModelSerializer):
    attempts = serializers.ListField()
    decision_time = serializers.ListField()

    class Meta:
        model = Result
        fields = ['user', 'attempts', 'decision_time']