from rest_framework import serializers
from django.contrib import auth
import time


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))


class BasicUserSerializer(serializers.ModelSerializer):
    date_joined = TimestampField(
        required=False,
        read_only=True,
    )
    last_login = TimestampField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = auth.get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'password',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True, 'required': False},
        }

    def create(self, validates_data):
        user = auth.get_user_model().objects.create(
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
