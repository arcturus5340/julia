from django.contrib import admin
from django.forms import widgets
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import Contest, Task, TestCase
from unixtimestampfield.fields import UnixTimeStampField


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_time', 'duration', 'tasks')
    search_fields = ('title', 'description')

    formfield_overrides = {
        UnixTimeStampField: { 'widget': widgets.DateTimeInput(attrs={'type': 'datetime-local'}) },
    }

    def tasks(self, obj):
        count = Task.objects.filter(contest=obj).count()
        url = (
            reverse('admin:contest_task_changelist')
            + '?'
            + urlencode({'contest__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} Tasks</a>', url, count)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'contest', '_order', 'content', 'human_ml', 'tl', 'test_cases')
    list_filter = ('contest',)
    search_fields = ('title', 'content')

    def human_ml(self, obj):
        size = obj.ml
        power = 2 ** 10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f'{int(size)} {power_labels[n]}bytes'

    def test_cases(self, obj):
        count = TestCase.objects.filter(task=obj).count()
        url = (
            reverse('admin:contest_testcase_changelist')
            + '?'
            + urlencode({'task__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} Test Cases</a>', url, count)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('input', 'output', 'task_link')
    list_filter = ('task', )
    search_fields = ('input', )

    def task_link(self, obj):
        url = (
            reverse('admin:contest_task_changelist')
            + '?'
            + urlencode({'id': f'{obj.task_id}'})
        )
        return format_html('<a href="{}">{}</a>', url, obj.task.title)
