from django.conf import settings
from django.core.files.storage import FileSystemStorage
import django_filters.rest_framework
from django.core import exceptions
from rest_framework import filters, permissions, status, viewsets
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.decorators import action

from contest import serializers
from contest.models import Contest, Task, TestCase, Solution, Result
from contest.permissions import ReadOnly

from checker.core import Checker
from django.utils import timezone


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser | ReadOnly]
    serializer_class = serializers.TaskSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'content']

    def get_queryset(self):
        return Task.objects.filter(contest__start_time__lte=timezone.now()).order_by('_order')

    def update(self, request, *args, **kwargs):
        partial_response = super().update(request, *args, **kwargs)
        if 'partial' in kwargs:
            return partial_response

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        task = serializer.save()
        test_cases = self.request.data.pop('test_cases', [])
        test_case_serializer = serializers.TestCaseSerializer(data=test_cases, many=True)
        test_case_serializer.is_valid(raise_exception=True)
        test_case_serializer.save(task_id=task.id)

    def perform_update(self, serializer):
        task = serializer.save()
        test_cases = self.request.data.pop('test_cases', [])
        test_case_serializer = serializers.TestCaseSerializer(data=test_cases, many=True)
        test_case_serializer.is_valid(raise_exception=True)
        test_case_serializer.save(task_id=task.id)


class ContestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser | ReadOnly]
    serializer_class = serializers.ContestSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Contest.objects.order_by('id')

    def update(self, request, *args, **kwargs):
        partial_response = super().update(request, *args, **kwargs)
        if 'partial' in kwargs:
            return partial_response

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=True)
    def results(self, request, pk, *args, **kwargs):
        queryset = Result.objects.filter(contest_id=pk).order_by('id')
        # TODO: Optimize sorting
        queryset = sorted(queryset, key=lambda result: (
            -len([x for x in result.attempts if x > 0]),
            sum(x for x in result.attempts if x > 0),
            sum(x for x in result.decision_time if x),
        ))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.ResultSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ResultSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Task.objects.filter(contest=instance).exists():
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=True)
    def tasks(self, request, *args, **kwargs):
        if self.get_object().start_time > timezone.now():
            queryset = []
        else:
            queryset = self.get_object().tasks.order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.TaskSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.TaskSerializer(queryset, many=True)
        return Response(serializer.data)


class SolutionViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser, FileUploadParser)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['author', 'task', 'status']

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [~permissions.AllowAny]
        elif self.action in ('create', ):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'retrieve'):
            serializer_class = serializers.SolutionDetailSerializer
        else:
            serializer_class = serializers.SolutionSerializer

        if 'context' in kwargs:
            kwargs['context'].update({'request': self.request})
        else:
            kwargs['context'] = {'request': self.request}
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        return Solution.objects.order_by('id')

    def create(self, request, *args, **kwargs):
        task_id = int(request.data.get('task'))
        if not Task.objects.filter(contest__start_time__lte=timezone.now(), id=task_id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        if 'code' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not {'lang', 'task'}.issubset(request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lang = request.data['lang']
        if lang not in Checker.SUPPORTED_LANGUAGES:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=task_id)
        except exceptions.ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        author = request.user

        code = request.FILES['code']
        fs = FileSystemStorage(
            location=settings.CODE_ROOT,
            base_url=settings.CODE_URL,
        )
        if lang == 'c':
            title = f'{author.username}_{task.id}_{timezone.now().strftime("%Y.%m.%d_%H.%M.%S")}.c'
        elif lang.startswith('cpp'):
            title = f'{author.username}_{task.id}_{timezone.now().strftime("%Y.%m.%d_%H.%M.%S")}.cpp'
        elif lang == 'pabc':
            title = f'{author.username}_{task.id}_{timezone.now().strftime("%Y.%m.%d_%H.%M.%S")}.pas'
        else:
            title = f'{author.username}_{task.id}_{timezone.now().strftime("%Y.%m.%d_%H.%M.%S")}'
        filename = fs.save(title, code)

        checker = Checker(f'{settings.CODE_URL}{filename}', lang, tl=task.tl, ml=task.ml)
        test_cases = TestCase.objects.filter(task=task).values_list('input', 'output')
        input, output = zip(*test_cases)
        checker.set_test_cases(input, output)
        result = checker.run()

        serialized_solution = {
            'author': author,
            'task': task,
            'status': list(result['status'].values())[-1],
            'details': result,
            'lang': lang,
            'code': f'{settings.CODE_URL}{filename}',
        }
        solution = serializer.save(**serialized_solution)
        if (timezone.now() < task.contest.start_time + task.contest.duration) and (serialized_solution['status'] != 'CE'):
            n_tasks = task.contest.tasks.count()
            obj, created = Result.objects.get_or_create(
                user=author,
                contest=task.contest,
                defaults={
                    'attempts': [0] * n_tasks,
                    'decision_time': [None] * n_tasks,
                },
            )
            if obj.attempts[task._order] <= 0:
                if serialized_solution['status'] == 'OK':
                    obj.attempts[task._order] = (-obj.attempts[task._order] or 1)
                    obj.decision_time[task._order] = int((timezone.now() - task.contest.start_time).total_seconds())
                else:
                    obj.attempts[task._order] -= 1
            obj.save()

        headers = {'Location': f'/solutions/{solution.id}'}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        contest = instance.task.contest
        if timezone.now() < contest.start_time + contest.duration:
            serializer = serializers.SolutionSerializer(instance)
        else:
            serializer = serializers.SolutionDetailSerializer(instance, context={'request': self.request})
        return Response(serializer.data)
