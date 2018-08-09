from django.db import models

from lookup_tables.models import AbstractLookupTable
from lookup_tables.fields import LookupField


class MyModelType(AbstractLookupTable):
    pass


class MyModelStatus(AbstractLookupTable):
    pass


class MyModelCategory(AbstractLookupTable):
    pass


class MyModel(models.Model):

    name = models.CharField(max_length=20)
    type = LookupField(MyModelType)
    status = LookupField(MyModelStatus)
    category = LookupField(MyModelCategory, null=True, blank=True)
