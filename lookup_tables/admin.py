from django.contrib import admin

from . import conf
from . import models


if conf.USE_ADMIN_SORTABLE2:
    from adminsortable2 import admin as sortableadmin
    class ItemsInlineBase(sortableadmin.SortableInlineAdminMixin, admin.TabularInline): pass  # noqa
else:
    LookupTableAdminBaseModel = admin.ModelAdmin
    class ItemsInlineBase(admin.TabularInline): pass  # noqa


@admin.register(models.LookupTable)
class LookupTableAdmin(admin.ModelAdmin):

    class ItemsInline(ItemsInlineBase):
        verbose_name = 'Item'
        model = models.LookupTableItem
        fields = ('name',) if conf.USE_ADMIN_SORTABLE2 else ('name', 'sort_order')
        extra = 1

    list_display = ('name',)

    fieldsets = (
        (
            None, {
                'fields': ('name',)
            }
        ),
    )

    inlines = (ItemsInline,)
