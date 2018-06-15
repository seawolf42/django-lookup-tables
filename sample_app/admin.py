from django.contrib import admin

from . import models


@admin.register(models.MyModel)
class MyModelAdmin(admin.ModelAdmin):

    list_display = ('name', 'type', 'status', 'category')
    fields = ('name', 'type', 'status', 'category')
