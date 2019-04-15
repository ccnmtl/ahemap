# Django settings for ahemap project.
import os.path
import platform
import sys

from ccnmtlsettings.shared import common


project = 'ahemap'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))


if platform.linux_distribution()[0] == 'Ubuntu':
    if platform.linux_distribution()[1] == '16.04':
        # 15.04 and later need this set, but it breaks
        # on trusty.
        # yeah, it's not really going to work on non-Ubuntu
        # systems either, but I don't know a good way to
        # check for the specific issue. Anyone not running
        # ubuntu will just need to set this to the
        # appropriate value in their local_settings.py
        SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
    elif platform.linux_distribution()[1] == '18.04':
        # On Debian testing/buster, I had to do the following:
        # * Install the sqlite3 and libsqlite3-mod-spatialite packages.
        # * Add the following to writlarge/local_settings.py:
        # SPATIALITE_LIBRARY_PATH =
        # '/usr/lib/x86_64-linux-gnu/mod_spatialite.so' I think the
        # django docs might be slightly out of date here, or just not
        # cover all the cases.
        #
        # I've found that Ubuntu 18.04 also works with this full path
        # to the library file, but not 'mod_spatialite'. I'll raise
        # this issue with Django.
        SPATIALITE_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/mod_spatialite.so'


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
    'infranil',
    'django_extensions',
    'django.contrib.gis',
    'rest_framework',
    'django.contrib.humanize',
    'ahemap.main',
]

ALLOWED_HOSTS = [
    'localhost',
    '.ctl.columbia.edu',
    '.ccnmtl.columbia.edu',
    'ahemap.veterans.columbia.edu',
]

MIDDLEWARE += [  # noqa
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]


THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'ahemap.main.views.django_settings')
TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'django.template.context_processors.csrf')

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
