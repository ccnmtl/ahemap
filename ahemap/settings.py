# flake8: noqa
from ahemap.settings_shared import *

try:
    from ahemap.local_settings import *
except ImportError:
    pass
