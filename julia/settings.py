"""
Django settings for julia project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import datetime
import os
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open("julia/config.yml", "r") as yml_file:
    config = yaml.load(yml_file, Loader=yaml.Loader)
    SECRET_KEY = config['django']['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'auth.apps.AuthConfig',
    'contest.apps.ContestConfig',
    'rating.apps.RatingConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'social_django',
    'rest_social_auth',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'moesifdjango.middleware.moesif_middleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CONN_MAX_AGE = 60

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

AUTH_USER_MODEL = 'custom_auth.User'

AUTHENTICATION_BACKENDS = [
    'auth.backends.VerificationBackend',
    'social_core.backends.github.GithubOAuth2'
]

with open("julia/config.yml", "r") as yml_file:
    config = yaml.load(yml_file, Loader=yaml.Loader)
    SOCIAL_AUTH_GITHUB_KEY = config['social']['github']['key']
    SOCIAL_AUTH_GITHUB_SECRET = config['social']['github']['secret']

ROOT_URLCONF = 'julia.urls'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)

EMAIL_TEMPLATES_URL = f'{MEDIA_URL}email_templates/'
EMAIL_TEMPLATES_ROOT = f'{MEDIA_ROOT}email_templates/'

TEMPLATES_URL = 'templates/'
TEMPLATES_ROOT = os.path.join(BASE_DIR, TEMPLATES_URL)

CODE_DIR = 'code/'
CODE_URL = f'{MEDIA_URL}code/'
CODE_ROOT = f'{MEDIA_ROOT}code/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [EMAIL_TEMPLATES_ROOT, TEMPLATES_ROOT],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'julia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
with open("julia/config.yml", "r") as yml_file:
    config = yaml.load(yml_file, Loader=yaml.Loader)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config['db']['name'],
            'USER': config['db']['user'],
            'PASSWORD': config['db']['password'],
            'HOST': config['db']['host'],
            'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Mail server data
with open("julia/config.yml", "r") as yml_file:
    config = yaml.load(yml_file, Loader=yaml.Loader)

    EMAIL_USE_TLS = config['email']['use_tls']
    EMAIL_HOST = config['email']['host']
    EMAIL_HOST_USER = config['email']['host_user']
    EMAIL_HOST_PASSWORD = config['email']['host_password']
    EMAIL_PORT = config['email']['port']

# Django REST framework configuration

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    # ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'PAGE_SIZE': 50,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1',
    'ALLOWED_VERSIONS': ('1', ),
    'VERSION_PARAM': 'version',
}

import datetime

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # Updating last_login will dramatically increase the number of database transactions.

    'AUTH_HEADER_TYPES': ('JWT', ),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}


# Activate Django-Heroku
import django_heroku
django_heroku.settings(locals())

# Activate Moesif
def identifyUser(req, res):
    if req.user and req.user.is_authenticated:
        return req.user.username
    else:
        return None

with open("julia/config.yml", "r") as yml_file:
    config = yaml.load(yml_file, Loader=yaml.Loader)
    MOESIF_MIDDLEWARE = {
        'APPLICATION_ID': config['moesif']['application_id'],
        'CAPTURE_OUTGOING_REQUESTS': False,
        'IDENTIFY_USER': identifyUser,
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)-8s [%(name)-12s]: %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(levelname)-8s [%(name)-12s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'julia.log'
        },
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.csrf': {
            'handlers': ['file'],
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['file'],
            'propagate': True,
        },
        'django.security.DisallowedRedirect': {
            'handlers': ['file'],
            'propagate': True,
        },
        'django.security.RequestDataTooBig': {
            'handlers': ['file'],
            'propagate': True,
        },
        'django.security.SuspiciousFileOperation': {
            'handlers': ['file'],
            'propagate': True,
        },
        'django.security.TooManyFieldsSent': {
            'handlers': ['file'],
            'propagate': True,
        },

    },
}
