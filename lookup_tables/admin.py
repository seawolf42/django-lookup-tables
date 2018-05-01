from django.contrib import admin

from . import models


@admin.register(models.LookupTable)
class LookupTableAdmin(admin.ModelAdmin):

    class ItemsInline(admin.TabularInline):
        verbose_name = 'Item'
        model = models.LookupTableItem
        fields = ('name',)
        extra = 3

    list_display = ('name',)

    fieldsets = (
        (
            None, {
                'fields': ('name',)
            }
        ),
    )

    inlines = (ItemsInline,)
