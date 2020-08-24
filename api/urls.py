from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),

    path('tasks/', views.TaskList.as_view()),
    path('tasks/<int:pk>', views.TaskDetail.as_view(), name='task-detail'),

    path('contests/', views.ContestList.as_view()),
    path('contests/<int:pk>', views.ContestDetail.as_view()),
]
