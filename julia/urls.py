from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from rest_framework import routers
import rest_framework_simplejwt.views

import auth.urls
import contest.urls
from julia.static import secure_serve


class ExtendableRouter(routers.DefaultRouter):
    def extend(self, router):
        self.registry.extend(router.registry)


router = ExtendableRouter()
router.extend(auth.urls.router)
router.extend(contest.urls.router)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token-auth', rest_framework_simplejwt.views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-refresh', rest_framework_simplejwt.views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('rest_social_auth.urls_jwt_pair')),
    path('api/', include(router.urls)),

    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'))

] + static(settings.CODE_DIR, document_root=settings.CODE_ROOT, view=secure_serve)