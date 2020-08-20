from django.shortcuts import render
from django.core.files.base import File

from contest.models import Code, Task
from django.contrib.auth.models import User

from datetime import datetime


def index(request):
    # if request.user.is_anonymous:
    #     return render(request, 'index.html')

    context = {
        'Tasks': Task.objects.all(),
    }

    if request.method == 'POST' and request.FILES['code-file']:
        user = User.objects.get(id=request.user.id)
        code = request.FILES['code-file']
        code.name = f'{user.username}_{datetime.now().strftime("%Y.%m.%d_%H.%M.%S")}'
        Code.objects.create(
            author=user,
            file=File(code),
        )

    return render(request, 'contest.html', context)