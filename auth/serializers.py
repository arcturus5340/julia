from django.contrib.auth.models import User
from rest_framework import serializers


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True, 'required': False},
        }

    def create(self, validates_data):
        user = User.objects.create(
            username=validates_data['username'],
            email=validates_data['email'],
        )
        user.set_password(validates_data['password'])
        user.save()
        return user

class FullUserSerializer(BasicUserSerializer):
    class Meta(BasicUserSerializer.Meta):
        extra_kwargs = BasicUserSerializer.Meta.extra_kwargs.copy()
        extra_kwargs.pop('email')
