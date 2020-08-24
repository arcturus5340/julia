from rest_framework import serializers

from django.contrib.auth.models import User
from contest.models import Contest, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'email', 'date_joined']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'contest', 'title', 'content']


class ContestSerializer(serializers.ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='task-detail'
    )
    class Meta:
        model = Contest
        fields = ['id', 'title', 'description', 'tasks']
