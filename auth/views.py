from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import django_filters.rest_framework
from django.contrib import auth
from django.utils import timezone

from rest_framework import filters
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import action

from auth import serializers
from auth.models import Activation, EmailTemplates
from auth.permissions import IsAdmin, IsOwner

import uuid
import re
import smtplib


def send_message(subject, html_message, user, email=None):
    from_email = settings.EMAIL_HOST_USER
    try:
        mail.send_mail(
            subject=subject,
            message='',
            html_message=html_message,
            from_email=from_email,
            recipient_list=[email or user.email],
        )
    except smtplib.SMTPException as err:
        return err.strerror


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    parser_classes = (MultiPartParser, JSONParser)
    # queryset = auth.get_user_model().objects.order_by('id')
    filterset_fields = ['username']
    search_fields = ['username']

    def get_queryset(self):
        return auth.get_user_model().objects.filter(groups__name='Verified Users').order_by('id')

    def get_serializer_class(self):
        if self.request.auth:
            return serializers.FullUserSerializer
        return serializers.BasicUserSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsAdmin | IsOwner]
        elif self.action in ('create', 'reset_password'):
            permission_classes = [~permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if not {'username', 'password', 'email'}.issubset(request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            activation_key = Activation.objects.create(
                user=user,
                key=uuid.uuid4().hex,
            )
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'email_template' not in request.data:
            filename = 'default_email_template.html'
        else:
            email_template = request.FILES['email_template']
            if not re.search(r'{{\s*link\s*}}' , email_template.read().decode()):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            fs = FileSystemStorage(
                location=settings.EMAIL_TEMPLATES_ROOT,
                base_url=settings.EMAIL_TEMPLATES_URL,
            )
            filename = fs.save(email_template.name, email_template)
            EmailTemplates.objects.create(template=filename)

        link = f'https://{request.get_host()}/api/v1/users/{user.id}/activation/{activation_key.key}'
        html_message = render_to_string(filename, {'link': link})

        fail_msg = send_message('Registration', html_message, user)
        if fail_msg:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = {'Location': f'/users/{user.id}'}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if 'partial' not in kwargs and not {'username', 'email', 'password'}.issubset(request.data.keys()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = self.get_object()

        password = request.data.pop('password', None)
        if password:
            if Activation.objects.filter(user=user, is_password_change=True).exists():
                return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

            try:
                activation_key = Activation.objects.create(
                    user=user,
                    key=uuid.uuid4().hex,
                    is_password_change=True,
                    tmp_data=make_password(password),
                )
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if 'email_template' not in request.data:
                filename = 'default_email_template.html'
            else:
                email_template = request.FILES['email_template']
                if not re.search(r'{{\s*link\s*}}', email_template.read().decode()):
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                fs = FileSystemStorage(
                    location=settings.EMAIL_TEMPLATES_ROOT,
                    base_url=settings.EMAIL_TEMPLATES_URL,
                )
                filename = fs.save(email_template.name, email_template)
                EmailTemplates.objects.create(template=filename)

            link = f'https://{request.get_host()}/api/v1/users/{user.id}/activation/{activation_key.key}'
            html_message = render_to_string(filename, {'link': link})

            fail_msg = send_message('Password Change', html_message, user)
            if fail_msg:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        email = request.data.pop('email', None)
        if isinstance(email, list): email = email.pop() # QueryDict handle
        if email:
            if Activation.objects.filter(user=user, is_email_change=True).exists():
                return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

            try:
                activation_key = Activation.objects.create(
                    user=user,
                    key=uuid.uuid4().hex,
                    is_email_change=True,
                    tmp_data=email,
                )
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if 'email_template' not in request.data:
                filename = 'default_email_template.html'
            else:
                email_template = request.FILES['email_template']
                if not re.search(r'{{\s*link\s*}}', email_template.read().decode()):
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                fs = FileSystemStorage(
                    location=settings.EMAIL_TEMPLATES_ROOT,
                    base_url=settings.EMAIL_TEMPLATES_URL,
                )
                filename = fs.save(email_template.name, email_template)
                EmailTemplates.objects.create(template=filename)

            link = f'https://{request.get_host()}/api/v1/users/{user.id}/activation/{activation_key.key}'
            html_message = render_to_string(filename, {'link': link})

            fail_msg = send_message('Email Change', html_message, user, email)
            if fail_msg:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = super().update(request, *args, **kwargs)
        if 'partial' in kwargs:
            return response
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password(self, request, *args, **kwargs):
        if 'password' not in request.data or not ({'username', 'email'} & request.data.keys()):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = auth.get_user_model().objects.filter(
            Q(username=request.data.get('username')) | Q(email=request.data.get('email'))
        ).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if Activation.objects.filter(user=user, is_password_change=True).exists():
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            activation_key = Activation.objects.create(
                user=user,
                key=uuid.uuid4().hex,
                is_password_change=True,
                tmp_data=make_password(request.data['password']),
            )
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'email_template' not in request.data:
            filename = 'default_email_template.html'
        else:
            email_template = request.FILES['email_template']
            if not re.search(r'{{\s*link\s*}}', email_template.read().decode()):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            fs = FileSystemStorage(
                location=settings.EMAIL_TEMPLATES_ROOT,
                base_url=settings.EMAIL_TEMPLATES_URL,
            )
            filename = fs.save(email_template.name, email_template)
            EmailTemplates.objects.create(template=filename)

        link = f'https://{request.get_host()}/activation/{user.username}/{activation_key.key}'
        html_message = render_to_string(filename, {'link': link})

        fail_msg = send_message('Password Change', html_message, user)
        if fail_msg:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True, url_path='activation/(?P<key>[0-9a-f]{32})')
    def activation(self, request, pk, key):
        activation_obj = Activation.objects.filter(user__id=pk, key=key).first()
        if not activation_obj:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)

        user = auth.get_user_model().objects.get(id=pk)
        if activation_obj.is_email_change:
            user.email = activation_obj.tmp_data
            user.save()
            activation_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if activation_obj.is_password_change:
            user.password = activation_obj.tmp_data
            user.save()
            activation_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if not user.last_login:
            user.date_joined = timezone.now()
            user.groups.add(Group.objects.get(name='Verified Users'))
            user.save()
            activation_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

