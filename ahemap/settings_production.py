# flake8: noqa
import sys
from django.conf import settings
from ahemap.settings_shared import *
from ctlsettings.production import common
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

locals().update(
    common(
        project=project,
        base=base,
        s3prefix='ccnmtl',
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
# if you use cloudfront:
#        cloudfront="justtheidhere",
# if you don't use S3/cloudfront at all:
#       s3static=False,
    ))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ahemap',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

try:
    from ahemap.local_settings import *
except ImportError:
    pass

if ('migrate' not in sys.argv) and \
   ('collectstatic' not in sys.argv) and \
   hasattr(settings, 'SENTRY_DSN'):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )
