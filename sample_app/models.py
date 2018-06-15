from django.db import models

from lookup_tables.fields import LookupTableItemField


class MyModel(models.Model):

    name = models.CharField(max_length=20)
    type = LookupTableItemField(table_ref='mymodel-type')
    status = LookupTableItemField(table_ref='mymodel-status')
    category = LookupTableItemField(table_ref='mymodel-category', null=True, blank=True)
