import os
import sys

from django.conf import settings


_SETTINGS = getattr(settings, 'LOOKUP_TABLES', {})

USE_ADMIN_SORTABLE2 = _SETTINGS.get('USE_ADMIN_SORTABLE2', False)
DRF_REPRESENTATION_NAME_NOT_ID = _SETTINGS.get('DRF_REPRESENTATION_NAME_NOT_ID', False)

IS_RUNNING_MANAGEMENT = len(sys.argv) > 1 and sys.argv[0].endswith('manage.py') and sys.argv[1] != 'runserver'

_IGNORE_INIT_RESET_KEY = 'LOOKUP_TABLES_DRF_FIELD_INIT_NO_RESET'

if _IGNORE_INIT_RESET_KEY in os.environ:
    IGNORE_INIT_RESET = os.environ[_IGNORE_INIT_RESET_KEY].lower() in ('1', 'true')
elif IS_RUNNING_MANAGEMENT:
    IGNORE_INIT_RESET = True
else:
    IGNORE_INIT_RESET = False

del _IGNORE_INIT_RESET_KEY
