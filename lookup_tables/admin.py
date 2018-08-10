from django.contrib import admin

from . import conf


if conf.USE_ADMIN_SORTABLE2:
    from adminsortable2 import admin as sortableadmin
    class LookupAdminBase(sortableadmin.SortableAdminMixin, admin.ModelAdmin): pass  # noqa
else:
    class LookupAdminBase(admin.ModelAdmin): pass  # noqa


class LookupAdmin(LookupAdminBase):
    pass
