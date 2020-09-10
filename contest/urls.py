import contest.views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', contest.views.TaskViewSet, basename='task')
router.register(r'contests', contest.views.ContestViewSet, basename='contest')
router.register(r'solutions', contest.views.SolutionViewSet, basename='solution')

urlpatterns = router.urls
