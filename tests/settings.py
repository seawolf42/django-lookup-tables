import django


DEBUG = True
USE_TZ = True

SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'lookup_tables',
    'sample_app',
)

LOOKUP_TABLES = {
    'USE_ADMIN_SORTABLE2': False,
    # 'DRF_REPRESENTATION_NAME_NOT_ID': True,
}

if LOOKUP_TABLES['USE_ADMIN_SORTABLE2']:
    INSTALLED_APPS = INSTALLED_APPS + ('adminsortable2',)

SITE_ID = 1

_middleware_list = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if django.VERSION >= (1, 10):
    MIDDLEWARE = _middleware_list
else:
    MIDDLEWARE_CLASSES = _middleware_list

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (),
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
)

APPEND_SLASH = True
STATIC_URL = '/static/'


#
# Django REST Framework config for local use
#

from rest_framework.authentication import SessionAuthentication  # noqa


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # disable all CSRF protections locally - DO NOT DO THIS IN PRODUCTION


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'tests.settings.CsrfExemptSessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}
