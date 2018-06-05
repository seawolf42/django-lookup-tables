from django.db import models as db_models

from . import models


class _lookup_table_item_choice_iterator(object):

    def __init__(self, table):
        self.items = models.LookupTableItem.objects.filter(table=table).iterator()

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self.items)
        return (item.id, item.name)

    def next(self):
        return self.__next__()


class _lookup_table_item_choices(object):

    def __init__(self, table):
        self.table = table

    def __iter__(self):
        return _lookup_table_item_choice_iterator(self.table)


class LookupTableItemField(db_models.Field):

    def __init__(self, table_ref, *args, **kwargs):
        self.table = models.LookupTable.objects.filter(table_ref=table_ref).first()
        if not self.table:
            self.table = models.LookupTable.objects.create(table_ref=table_ref, name=table_ref)
        super(LookupTableItemField, self).__init__(*args, **kwargs)
