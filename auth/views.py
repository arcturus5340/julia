from django.contrib import auth
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from django.conf import settings
from django.core import mail

from contest.views import index

import smtplib


def send_message(subject: str, message: str, user: User):
    from_email = settings.EMAIL_HOST_USER
    try:
        mail.send_mail(subject, message, from_email, [user.email])
    except smtplib.SMTPException as err:
        return JsonResponse({
            'status': 'fail',
            'message': 'error sending activation email',
        })


def login(request):
    user = auth.authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password'),
    )
    if user is not None:
        auth.login(request, user)
    else:
        pass

    return JsonResponse({
        'status': 'ok',
        'content': render_to_string('contest.html'),
    })


def logout(request):
    auth.logout(request)


def registration(request):
    if User.objects.filter(username=request.POST.get('username')).exists():
        return JsonResponse({
            'status': 'fail',
            'reason': 'username is not unique',
        })
    if User.objects.filter(email=request.POST.get('email')).exists():
        return JsonResponse({
            'status': 'fail',
            'reason': 'email is not unique',
        })

    try:
        User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
    except Exception as err:
        pass

    return change_to_login_form(request)


def reset_password(request):
    pass


def change_to_login_form(request):
    return JsonResponse({
        'status': 'ok',
        'content': render_to_string('login_form.html'),
    })

def change_to_registration_form(request):
    return JsonResponse({
        'status': 'ok',
        'content': render_to_string('registration_form.html'),
    })

def change_to_reset_form(request):
    return JsonResponse({
        'status': 'ok',
        'content': render_to_string('reset_password_form.html'),
    })
