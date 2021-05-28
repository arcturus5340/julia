from django.contrib.auth.models import Group

from social_core.pipeline.partial import partial


@partial
def verify_user(strategy, details, user=None, is_new=False, *args, **kwargs):
    user.groups.add(Group.objects.get(name='Verified Users'))
    user.save()