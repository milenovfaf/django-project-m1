"""
Django settings for web_site project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import ugettext_lazy as _
# ------------------------------------------------------------------------------
SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7
MONTH = DAY * 30
YEAR = DAY * 365

# ##############################################################################

# https://docs.python.org/3/library/time.html#time.strftime
# 2013-02-25 18:25:10 +03:00
API_DATE_FORMAT = '%Y-%m-%dT'
# from datetime import datetime
# datetime.isoformat()
#         """Return the time formatted according to ISO.
#
#         The full format looks like 'YYYY-MM-DD HH:MM:SS.mmmmmm'.
#         By default, the fractional part is omitted if self.microsecond == 0.
#
#         If self.tzinfo is not None, the UTC offset is also attached, giving
#         giving a full format of 'YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM'.
#
#         Optional argument sep specifies the separator between date and
#         time, default 'T'.
#
#         The optional argument timespec specifies the number of additional
#         terms of the time to include.
#         """

# YYYY-MM-DDThh:mm:ssZ              2020-11-18T01:44:29+0000
# 2020-12-01T12:00:00+03:00         2020-11-18T01:44:29.223764Z
# https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#std:templatefilter-date
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

OWN_DATE_FORMAT = '%Y-%m-%d'
OWN_TIME_FORMAT = '%H:%M:%S'
OWN_DATETIME_FORMAT = f'{OWN_DATE_FORMAT}T{OWN_TIME_FORMAT}%z'


# ##############################################################################

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

APP_NAME = os.environ.get('APP_NAME', os.path.basename(BASE_DIR))

RELEASE_NAME = os.environ.get('RELEASE_NAME')
GIT_CURRENT_REF = os.environ.get('GIT_CURRENT_REF')


# all service files of django: static, media, logs, etc.
SITE_DIR = os.environ.get(
    'SITE_DIR',
    os.path.abspath(os.path.join(BASE_DIR, '../../data', APP_NAME))
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', 'False') == 'True')


STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(SITE_DIR, 'static'))
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ALLOWED_HOSTS = ['*']


_allowed_hosts = os.environ.get('ALLOWED_HOSTS', '').lower()
if _allowed_hosts:
    import re
    for _host in re.sub(r'[^a-zA-Z0-9\-.\*]+', ',', _allowed_hosts).split(','):
        if _host:
            ALLOWED_HOSTS.append(_host)


# Application definition
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'app_common',  # runserver disable check migrations for dockerfile
    'django.contrib.staticfiles',

    'debug_toolbar',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'app04_movies',
    'app05_contact',

    'ckeditor_uploader',
    'ckeditor',
    

    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.vk',
]

# ?????? debug_toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '[::1]',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

WSGI_APPLICATION = 'web_site.wsgi.application'
ROOT_URLCONF = 'web_site.urls'


'''???????????? TemplateDoesNotExist - ???????????????????? ?????????? ????????????, ???????????? ?????????? ???? 
?????????? ?????????????? ???????? ???????????? 'DIRS' ????????????
BASE_DIR - ???????????????????? ???????????????? ???????????? ???????? ?? ?????????? ??????????????, 
templates - ???????????????????? ?? ??????????????????.
APP_DIRS - ???????????????? ?????????? ???? ???????????? ???????? ??????????????
'''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],  # [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #     # django.core.exceptions.ImproperlyConfigured:
            #     # app_dirs must not be set when loaders is defined.
            #     # https://stackoverflow.com/questions/10386257/tell-django-to-search-apps-template-subfolders
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            #     # https://django-admin-tools.readthedocs.io/en/latest/quickstart.html#configuration
            #     # https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/
            # ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        # docker run -d --name pg_dj_zum -e POSTGRES_PASSWORD=postgres -p 0.0.0.0:15432:5432  postgres
        'ENGINE':       'django.db.backends.postgresql_psycopg2',
        'NAME':         os.environ.get('DB_NAME',       'postgres'),
        'USER':         os.environ.get('DB_USER',       'postgres'),
        'PASSWORD':     os.environ.get('DB_PASSWORD',   'postgres'),
        'HOST':         os.environ.get('DB_HOST',       'localhost'),
        'PORT':         os.environ.get('DB_PORT',        '5432'),
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = True
# ------------------------------------------------------------------------------

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]
TIME_ZONE = 'UTC'
USE_I18N = True
# https://stackoverflow.com/questions/1004109/how-do-i-make-djangos-datetime-format-active
USE_L10N = False
USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i O'
# DATE_FORMAT = 'Y-m-d'
# TIME_FORMAT = 'H:i O'

# ------------------------------------------------------------------------------
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# ------------------------------------------------------------------------------
CKEDITOR_UPLOAD_PATH = "uploads/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(SITE_DIR, 'static'))
# https://stackoverflow.com/questions/7456817/django-when-should-i-use-media-root-or-static-root
MEDIA_ROOT = os.path.join(SITE_DIR, 'media')
STATICFILES_FINDERS = (
    # http://djbook.ru/examples/33/
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
ADMIN_MEDIA_PREFIX = '/static/admin/'
# https://docs.djangoproject.com/en/2.1/ref/settings/#append-slash

LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING').strip().upper()
LOG_DIR = os.path.join(SITE_DIR, 'log')

LOG_FORMAT = (
    'DJANGO: %(asctime)s |'
    # '%(thread)s |'
    # '[ %(pathname)-110s ]'
    '%(module)-20s '  # python.module.path
    'line:%(lineno)4d | '  # code line-number
    'fn: %(funcName)-20s '
    '| %(name)-25s '                    # logging-name
    '%(levelname)-7s'
    ' :    %(message)s'
)
LOG_DATE_FORMAT = '%m.%d %H:%M:%S'


# https://docs.djangoproject.com/en/2.1/topics/logging/#examples
# https://lincolnloop.com/blog/django-logging-right-way/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format':   LOG_FORMAT,
            'datefmt':  LOG_DATE_FORMAT,
        },
    },

    'handlers': {
        'console': {
            'class':        'logging.StreamHandler',
            'level':        'DEBUG',
            'formatter':    'verbose'
        },
    },

    'loggers': {
        '': {
            'handlers':     [
                'console',
                'sentry',
            ],
            'level':        LOG_LEVEL,
            'propagate':    False,
        },
        # - - -
        'django':           {'level': 'WARNING', 'propagate': False, 'handlers':['console', 'sentry', ]},
        'django.request':   {'level': 'WARNING', 'propagate': False, 'handlers':['console', 'sentry', ]},
        # - - -
        'app_leads':        {'level': 'DEBUG',   'propagate': False, 'handlers':['console', 'sentry', ]},
        'app_common':       {'level': 'DEBUG',   'propagate': False, 'handlers':['console', 'sentry', ]},
    },
}

# ------------------------------------------------------------------------------
SITE_ID = 1

# import dj_database_url
# prod_db=dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(prod_db)


print('USING BASE SETTINGS!')