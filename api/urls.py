from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'solutions', views.SolutionViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'contests', views.ContestViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('users/', views.UserList.as_view()),
#     path('users/<int:pk>', views.UserDetail.as_view()),
#     # path('users/<int:pk>/', views.UserDetail.as_view()),
#
#     path('tasks/', views.TaskList.as_view()),
#     path('tasks/<int:pk>', views.TaskDetail.as_view(), name='task-detail'),
#
#     path('contests/', views.ContestList.as_view()),
#     path('contests/<int:pk>', views.ContestDetail.as_view()),
#
#     path('solutions/<int:pk>', views.SolutionDetail.as_view(), name='solution-detail'),
# ]
