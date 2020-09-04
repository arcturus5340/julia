from rest_framework import serializers

from django.contrib.auth.models import User
from contest.models import Contest, Task, Solution


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = read_only_fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'last_login',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True},
            # 'email': {'write_only': True},
        }

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.username)
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
        ]
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'email': {'required': True},
        }

    def create(self, validates_data):
        user = User.objects.create(
            username=validates_data['username'],
            email=validates_data['email'],
        )
        user.set_password(validates_data['password'])
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    contest = serializers.HyperlinkedRelatedField(
        view_name='contest-detail',
        queryset=Task.objects.all(),
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'content', 'contest', 'tl', 'ml']
        read_only_fields = ['id', 'samples']
        extra_kwargs = {
            'samples': {'source': 'get_samples'}
        }

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.update(**validated_data)


class ContestSerializer(serializers.ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='task-detail',
    )

    class Meta:
        model = Contest
        fields = ['title', 'description', 'tasks']
        read_only_fields = ['id']

    def create(self, validated_data):
        return Contest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.update(**validated_data)


class SolutionSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
    )
    task = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='task-detail',
    )
    contest = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='contest-detail',
    )

    class Meta:
        model = Solution
        fields = read_only_fields = ['id', 'author', 'task', 'contest', 'status', 'file']

    def create(self, validated_data):
        return Solution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.update(**validated_data)
