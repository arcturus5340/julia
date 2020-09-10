"""julia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken.views import obtain_auth_token
import rest_framework_jwt.views

import contest.views
import auth.views

from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', auth.views.UserViewSet)
# router.register(r'solutions', views.SolutionViewSet)
# router.register(r'tasks', views.TaskViewSet)
# router.register(r'contests', views.ContestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('auth/registration/', auth.views.registration),
    # path('auth/reset-password/', auth.views.reset_password),

    # path('activate/<str:username>/<str:key>', auth.views.activate),

    path('api/token-auth', rest_framework_jwt.views.obtain_jwt_token),
    path('api/token-refresh', rest_framework_jwt.views.refresh_jwt_token),

    path('api/v1/', include(router.urls)),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('check-solution/', contest.views.check_solution),
]
