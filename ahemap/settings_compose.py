# flake8: noqa
from ahemap.settings_shared import *
from ctlsettings.compose import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))

try:
    from ahemap.local_settings import *
except ImportError:
    pass
