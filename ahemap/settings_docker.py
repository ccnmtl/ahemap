# flake8: noqa
from ahemap.settings_shared import *
from ctlsettings.docker import common
import os

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))
