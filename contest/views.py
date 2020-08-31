from django.shortcuts import render
from django.http.response import JsonResponse
from django.core.files.base import File

from contest.models import Contest, Task, TestCase, Solution
from django.contrib.auth.models import User

from datetime import datetime
from checker.core import Checker


def index(request):
    # if request.user.is_anonymous:
    #     return render(request, 'auth.html')

    return render(request, 'contest.html', {
        'Tasks': Task.objects.all(),
    })


def check_solution(request):
    code = request.FILES['file']
    lang = request.POST['language']
    task_id = int(request.POST['task'])
    user = User.objects.get(id=request.user.id)

    code.name = f'{user.username}_{datetime.now().strftime("%Y.%m.%d_%H.%M.%S")}'
    contest = Contest.objects.get(id=1)
    code = Solution.objects.create(
        author=user,
        contest=contest,
        task=Task.objects.get(id=task_id),
        status='Bal-bla',
        file=File(code),
    )

    checker = Checker(code.file.path, lang)
    test_cases = TestCase.objects.filter(task_id=task_id).values_list('input', 'output')
    input, output = zip(*test_cases)
    checker.set_test_cases(input, output)
    response = checker.run()

    return JsonResponse({
        'status': 'ok',
        'code': 0x00,
        'content': response,
    })
