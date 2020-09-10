from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
import rest_framework_jwt.views

import auth.urls
import contest.urls


class ExtendableRouter(routers.DefaultRouter):
    def extend(self, router):
        self.registry.extend(router.registry)


router = ExtendableRouter()
router.extend(auth.urls.router)
router.extend(contest.urls.router)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token-auth', rest_framework_jwt.views.obtain_jwt_token),
    path('api/token-refresh', rest_framework_jwt.views.refresh_jwt_token),

    path('api/v1/', include(router.urls)),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
] + static(settings.CODE_DIR, document_root=settings.CODE_ROOT)