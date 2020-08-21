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
from django.urls import path

import contest.views
import auth.views


urlpatterns = [
    path('', contest.views.index),
    path('admin/', admin.site.urls),

    path('login/', auth.views.login),
    path('logout/', auth.views.logout),
    path('registration/', auth.views.registration),
    path('reset-password/', auth.views.reset_password),

    path('login/change-to-login-form/', auth.views.change_to_login_form),
    path('login/change-to-registration-form/', auth.views.change_to_registration_form),
    path('login/change-to-reset-form/', auth.views.change_to_reset_form),

]
