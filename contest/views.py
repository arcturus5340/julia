from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from contest.models import Code, Task


def index(request):
    # if request.user.is_anonymous:
    #     return render(request, 'index.html')

    context = {
        'Tasks': Task.objects.all(),
    }

    if request.method == 'POST' and request.FILES['code-file']:
        code = request.FILES['code-file']
        fs = FileSystemStorage()
        filename = fs.save(code.name, code)
        Code.objects.create_by_filename(filename)

    return render(request, 'contest.html', context)