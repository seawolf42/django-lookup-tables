from django.db import models as db_models

from . import models


class LookupTableItemField(db_models.Field):

    def __init__(self, table_ref, *args, **kwargs):
        self.table = models.LookupTable.objects.filter(table_ref=table_ref).first()
        if not self.table:
            self.table = models.LookupTable.objects.create(table_ref=table_ref, name=table_ref)
        super(LookupTableItemField, self).__init__(*args, **kwargs)
