from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rating.models import History


@receiver(post_save, sender=User)
def create_rating_history_record(sender, instance, created, **kwargs):
    if created:
        History.objects.create(user=instance)
