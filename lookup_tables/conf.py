from django.conf import settings

_SETTINGS = getattr(settings, 'LOOKUP_TABLES', {})

USE_ADMIN_SORTABLE2 = _SETTINGS.get('USE_ADMIN_SORTABLE2', False)
