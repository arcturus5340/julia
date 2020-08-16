from django.shortcuts import render

from contest.models import Task


def index(request):
    if request.user.is_anonymous:
        return render(request, 'index.html')

    context = {
        'Tasks': Task.objects.all(),
    }

    return render(request, 'contest.html', context)