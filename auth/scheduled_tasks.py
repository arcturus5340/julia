from auth.models import Activation, EmailTemplates
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib import auth


def delete_old_activation_keys():
    Activation.objects.filter(created__gt=timezone.now()-timezone.timedelta(days=1)).delete()


def delete_old_email_templates():
    EmailTemplates.objects.filter(created__gt=timezone.now()-timezone.timedelta(days=1)).delete()


def delete_unverified_users():
    auth.get_user_model().objects.exclude(groups__name='Verified Users').delete()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_old_activation_keys, 'interval', days=1)
    scheduler.add_job(delete_old_email_templates, 'interval', days=1)
    scheduler.add_job(delete_unverified_users, 'interval', days=1)
    scheduler.start()
