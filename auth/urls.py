import auth.views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', auth.views.UserViewSet, basename='user')

urlpatterns = router.urls
