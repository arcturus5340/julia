from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.contrib import auth
from django.conf import settings
from django.template.loader import render_to_string
from django.core import mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets

from api import serializers
from auth.models import ActivationKeys

from contest.models import Contest, Task, Solution

import uuid
import smtplib


def send_message(subject: str, message: str, html_message: str, user: User):
    from_email = settings.EMAIL_HOST_USER
    try:
        mail.send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=from_email,
            recipient_list=[user.email],
        )
    except smtplib.SMTPException as err:
        return err.strerror


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('id')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.auth:
            return serializers.UserSerializer
        return serializers.BasicUserSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = serializers.UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         try:
    #             activation_key = ActivationKeys.objects.create(
    #                 user=user,
    #                 key=uuid.uuid4().hex,
    #                 is_email_verification=True,
    #             )
    #         except Exception:
    #             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    #         link = f'https://{settings.DOMAIN}/activation/{user.username}/{activation_key.key}'
    #         html_message = render_to_string('email_templates/registration-message.html', {'link': link})
    #         fail_msg = send_message('Registration', '', html_message, user)
    #         if fail_msg:
    #             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserDetail(viewsets.ModelViewSet):
#     serializer_class = serializers.UserSerializer
#     queryset = User.objects.order_by('id')
#
#     def get_permissions(self):
#         if self.action == 'list':
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [AllowAny]
#         return [permission() for permission in permission_classes]
#
#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = serializers.UserDetailSerializer(user)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = serializers.UserDetailSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.order_by('id')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    #
    # def get(self, request, format=None):
    #     tasks = Task.objects.all()
    #     serializer = serializers.TaskSerializer(tasks, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = serializers.TaskSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TaskDetail(viewsets.ViewSet):
#     def get_object(self, pk):
#         try:
#             return Task.objects.get(pk=pk)
#         except Task.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = serializers.TaskSerializer(task)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = serializers.TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ContestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContestSerializer
    queryset = Contest.objects.order_by('id')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    # def get(self, request, format=None):
    #     contests = Contest.objects.all()
    #     serializer = serializers.ContestSerializer(contests, many=True, context={'request': request})
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = serializers.ContestSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ContestDetail(viewsets.ViewSet):
#     def get_object(self, pk):
#         try:
#             return Contest.objects.get(pk=pk)
#         except Contest.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         contest = self.get_object(pk)
#         serializer = serializers.ContestSerializer(contest, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         contest = self.get_object(pk)
#         serializer = serializers.ContestSerializer(contest, context={'request': request}, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         contest = self.get_object(pk)
#         contest.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class SolutionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SolutionSerializer
    queryset = Solution.objects.order_by('id')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    #
    # def get(self, request, format=None):
    #     solutions = Solution.objects.all()
    #     serializer = serializers.SolutionSerializer(solutions, many=True, context={'request': request})
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = serializers.SolutionSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SolutionDetail(viewsets.ViewSet):
#     def get_object(self, pk):
#         try:
#             return Solution.objects.get(pk=pk)
#         except Solution.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         solution = self.get_object(pk)
#         serializer = serializers.SolutionDetailSerializer(solution, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         solution = self.get_object(pk)
#         serializer = serializers.SolutionDetailSerializer(solution, context={'request': request}, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         solution = self.get_object(pk)
#         solution.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
