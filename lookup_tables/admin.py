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
        fields = ('name',) if conf.USE_ADMIN_SORTABLE2 else ('name', 'sort_order', 'is_default')
        readonly_fields = ('is_default',)
        extra = 1

    list_display = ('name',)

    fieldsets = (
        (
            None, {
                'fields': ('name', 'default')
            }
        ),
    )

    inlines = (ItemsInline,)

    def has_add_permission(self, request):
        return False

    def render_change_form(self, request, context, *args, **kwargs):
        item = kwargs['obj']
        if item is not None and item.id > 0:
            context['adminform'].form.fields['default'].queryset = models.LookupTableItem.objects.filter(table=item)
        return super(LookupTableAdmin, self).render_change_form(request, context, *args, **kwargs)
