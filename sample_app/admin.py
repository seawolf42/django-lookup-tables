from django.contrib import admin

from . import models


@admin.register(models.MyModel)
class MyModelAdmin(admin.ModelAdmin):

    list_display = ('name', 'status', 'category')
    fields = ('name', 'status', 'category')
