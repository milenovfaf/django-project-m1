import os
from datetime import timedelta

os.environ.setdefault(
    'SECRET_KEY',
    'django-insecure-r_6hz41%v#2u2wzxr7z5%$ypxvn4f+26bth3267ewhqc3mie&f',
)
os.environ.setdefault(
    'RELEASE_NAME',
    'LOCAL_DEVELOPMENT',
)

os.environ.setdefault('DEBUG', '1')

# ------------------------------------------------------------------------------
from .base import *

if not os.path.exists(SITE_DIR):
    os.makedirs(SITE_DIR)
#
if not os.path.exists(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)
#
# if not os.path.exists(MEDIA_ROOT):
#     os.mkdir(MEDIA_ROOT)
#

# MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles') # HEROKUЫ
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
#

ALLOWED_HOSTS = ['*']

# https://github.com/adamchainz/django-cors-headers#cors_allow_credentials
# CORS_ALLOW_ALL_ORIGINS = True

# https://stackoverflow.com/questions/43002444/make-axios-send-cookies-in-its-requests-automatically/43178070
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
#     "http://127.0.0.1:8080",
#     "http://localhost:9000",
#     "http://127.0.0.1:9000",
# ]
CORS_ORIGIN_REGEX_WHITELIST = [
    "http://localhost[^.]+",
    "http://127.0.0.1[^.]+",
]
#
# # https://github.com/adamchainz/django-cors-headers#cors_allow_headers
# # https://github.com/adamchainz/django-cors-headers/issues/579
# CORS_ALLOW_HEADERS = list(default_headers) + [
#     'access-control-allow-origin',
# ]

# https://github.com/adamchainz/django-cors-headers#cors_preflight_max_age
CORS_PREFLIGHT_MAX_AGE = 2 * SECOND
# ------------------------------------------------------------------------------

DEBUG = True

DATABASES = {
    # docker run -d --name pg_movies_20220824 -e POSTGRES_PASSWORD=postgres -p 127.0.0.1:5432:5432 postgres
    'default': {
        'ENGINE':       'django.db.backends.postgresql_psycopg2',
        'NAME':         os.environ.get('DB_NAME',       'postgres'),
        'USER':         os.environ.get('DB_USER',       'postgres'),
        'PASSWORD':     os.environ.get('DB_PASSWORD',   'postgres'),
        'HOST':         os.environ.get('DB_HOST',       'localhost'),
        'PORT':         os.environ.get('DB_PORT',        '5432'),
    }
}

# ------------------------------------------------------------------------------

ROOT_URLCONF = 'web_site.urls_dev'
# ------------------------------------------------------------------------------


_KB = 1024
_MB = _KB * 1024


# https://docs.djangoproject.com/en/2.1/topics/logging/#examples
# https://lincolnloop.com/blog/django-logging-right-way/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'class':    'utils.logging.Formatter',
            'format':   LOG_FORMAT,
            'datefmt':  LOG_DATE_FORMAT,
        },

        'detail_trice': {
            'class':    'utils.logging.DetailFormatter',
            'format':   LOG_FORMAT,
            'datefmt':  LOG_DATE_FORMAT,
        },
    },

    'handlers': {
        'console': {
            'class':        'logging.StreamHandler',
            'level':        'DEBUG',
            'formatter':    'verbose',
        },

        'file_debug': {
            'class':        'logging.handlers.RotatingFileHandler',
            'level':        'DEBUG',
            'formatter':    'verbose',
            'filename':     os.path.join(
                LOG_DIR, '{}.django.debug.log'.format(APP_NAME)),
            'mode':         'a',
            'encoding':     'utf-8',
            'maxBytes':     _MB * 10,
            'backupCount':  1,
        },

        'file_error': {
            'class':        'logging.handlers.RotatingFileHandler',
            'level':        'ERROR',
            'formatter':    'verbose',
            'filename':     os.path.join(
                LOG_DIR, '{}.django.error.log'.format(APP_NAME)),
            'mode':         'a',
            'encoding':     'utf-8',
            'maxBytes':     _MB * 10,
            'backupCount':  1,
        },

        'file_error_detail_trice': {
            'class':        'logging.handlers.RotatingFileHandler',
            'level':        'ERROR',
            'formatter':    'detail_trice',
            'filename':     os.path.join(
                LOG_DIR, '{}.django.error.detail.log'.format(APP_NAME)),
            'mode':         'a',
            'encoding':     'utf-8',
            'maxBytes':     _MB * 10,
            'backupCount':  1,
        },
    },

    'loggers': {
        '': {
            'handlers':     [
                'console',
                'file_debug',
                'file_error',
                'file_error_detail_trice',
            ],
            'level':        'INFO',
            'propagate':    False,
        },
        # - - -
        'django':           {'level': 'INFO', 'propagate': True, },
        'django.request':   {'level': 'DEBUG', 'propagate': True, },
        # - - -
        'app_leads':        {'level': 'DEBUG', 'propagate': True, },
    },
}
# ------------------------------------------------------------------------------


CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
                # 'Youtube'

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            # 'youtube'
        ]),
    }
}


# ------------------------------------------------------------------------------
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,  # Подтверждение email
    'SERIALIZERS': {},
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


