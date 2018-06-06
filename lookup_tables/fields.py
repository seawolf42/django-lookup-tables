from django.db import models as db_models

from . import models


class LookupTableItemField(db_models.ForeignKey):

    def __init__(self, table_ref, *args, **kwargs):
        self.table_ref = table_ref
        self.lookuptable = models.LookupTable.objects.filter(table_ref=table_ref).first()
        if not self.lookuptable:
            self.lookuptable = models.LookupTable.objects.create(table_ref=table_ref, name=table_ref)
            models.LookupTableItem.objects.create(table=self.lookuptable, name='<DEFAULT>')
        kwargs['to'] = 'lookup_tables.LookupTableItem'
        kwargs['on_delete'] = db_models.PROTECT
        kwargs['limit_choices_to'] = self.get_lookuptableitem_choices
        super(LookupTableItemField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(LookupTableItemField, self).deconstruct()
        if 'limit_choices_to' in kwargs:
            del kwargs['limit_choices_to']
        kwargs['table_ref'] = self.table_ref
        return name, path, args, kwargs

    def get_lookuptableitem_choices(self):
        return db_models.Q(table=self.lookuptable)
