from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from django.conf import settings
from django.core import mail
from django.shortcuts import redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from auth.models import ActivationKeys

import smtplib
import uuid


# from django.contrib.auth.decorators import user_passes_test
#
# def group_required(*group_names):
#     """Requires user membership in at least one of the groups passed in."""
#     def in_groups(user):
#         if user.is_authenticated():
#             if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
#                 return True
#         return False
#
#     return user_passes_test(in_groups, login_url='/')


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


def reset_password(request):
    user = User.objects.filter(
        Q(username=request.POST.get('user-key')) | Q(email=request.POST.get('user-key'))
    ).first()

    if not user:
        return JsonResponse({
            'status': 'fail',
            'code': 0x06,
            'reason': 'unregistered user',
        })

    activation_key = ActivationKeys.objects.create(
        user=user,
        key=uuid.uuid4().hex,
        is_password_reset=True,
    )

    link = f'https://{settings.DOMAIN}/activation/{user.username}/{activation_key.key}'

    html_message = render_to_string('email_templates/reset-password-message.html', {'link': link})
    fail_msg = send_message('Password reset', '', html_message, user)
    if fail_msg:
        return JsonResponse({
            'status': 'fail',
            'code': 0x07,
            'reason': 'reset password message error',
        })

    return JsonResponse({
        'status': 'ok',
        'code': 0x00,
    })


def activate(request, username, key):
    user = User.objects.filter(username=username).first()
    activation_key = ActivationKeys.objects.filter(key=key, user=user).first()
    if not activation_key:
        return JsonResponse({
            'status': 'fail',
            'code': 0x08,
            'reason': 'activation_key not exists',
        })

    if activation_key.is_password_reset:
        pass

    if activation_key.is_email_verification:
        verified_users = Group.objects.get(name='Verified Users')
        verified_users.user_set.add(user)

        return redirect('/')
