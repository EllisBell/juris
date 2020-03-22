"""
Django settings for juris project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import raven
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('JURIS_SECRET', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['188.166.101.76', 'jurisprudencia.pt', 'www.jurisprudencia.pt', '127.0.0.1']

SITE_ID = 1

MIGRATION_MODULES = {
    'sites': 'juris.fixtures.sites_migrations',
}

# Application definition

INSTALLED_APPS = [
    'jurisapp.apps.JurisappConfig',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'juris.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'juris.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jurisdb',
        'USER': 'jurisuser',
        'PASSWORD': os.environ.get('JURIS_DB_PW', ''),
        'HOST': 'localhost',
        'CONN_MAX_AGE': 600,
    }
}

AUTH_USER_MODEL = 'jurisapp.user'

LOGIN_URL = 'juris_login'

LOGIN_REDIRECT_URL = 'dossier_home'

LOGOUT_REDIRECT_URL = 'juris_index'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'pt-PT'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Celery config
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'scheduled_indexing_task': {
        'task': 'jurisapp.tasks.bulk_index_task',
        'schedule': crontab(hour=4, minute=0)
    },
    'full_reindexing_task': {
        'task': 'jurisapp.tasks.recreate_index_from_db',
        'schedule': crontab(hour=9, minute=0, day_of_week=6)
    }
}

# Raven/Sentry (error logging) config
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_KEY', ''),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}

# Email config
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.eu'
EMAIL_HOST_USER = os.environ.get('ADMIN_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('JURIS_EMAIL_PW')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL='info@jurisprudencia.pt'