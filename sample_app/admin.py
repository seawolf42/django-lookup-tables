from django.contrib import admin
from lookup_tables.admin import LookupAdmin

from . import models


@admin.register(models.MyModelCategory)
class MyModelCategory(LookupAdmin):
    pass


@admin.register(models.MyModelStatus)
class MyModelStatus(LookupAdmin):
    pass


@admin.register(models.MyModelType)
class MyModelType(LookupAdmin):
    pass


@admin.register(models.MyModel)
class MyModelAdmin(admin.ModelAdmin):

    list_display = ('name', 'type', 'status', 'category')
    fields = ('name', 'type', 'status', 'category')
