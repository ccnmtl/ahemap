# Django settings for ahemap project.
import os.path
import sys

from ctlsettings.shared import common

project = 'ahemap'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ahemap',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
        'ATOMIC_REQUESTS': True,
    }
}

if ('test' in sys.argv or 'jenkins' in sys.argv or 'validate' in sys.argv
        or 'check' in sys.argv):
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
            'ATOMIC_REQUESTS': True,
        }
    }


PROJECT_APPS = [
    'ahemap.main',
]

USE_TZ = True

INSTALLED_APPS += [  # noqa
    'bootstrap4',
    'django_extensions',
    'django.contrib.gis',
    'rest_framework',
    'django.contrib.humanize',
    'ahemap.main',
]

ALLOWED_HOSTS += [ # noqa
    'ahemap.veterans.columbia.edu',
]

MIDDLEWARE += [  # noqa
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(base, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'stagingcontext.staging_processor',
                'gacontext.ga_processor',
                'ahemap.main.views.django_settings',
                'django.template.context_processors.csrf'
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'ahemap.main.utils.BrowsableAPIRendererNoForms'
    ),
    'PAGINATE_BY': 15,
    'DATETIME_FORMAT': '%m/%d/%y %I:%M %p'
}

JIRA_CONFIGURATION = ''  # specify in production

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
