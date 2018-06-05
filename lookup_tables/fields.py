from django.db import models as db_models

from . import models


class _lookup_table_item_choice_iterator(object):

    def __init__(self, lookuptable):
        self.items = models.LookupTableItem.objects.filter(table=lookuptable).iterator()

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self.items)
        return (item.id, item.name)

    def next(self):
        return self.__next__()


class _lookup_table_item_choices(object):

    def __init__(self, lookuptable):
        self.lookuptable = lookuptable

    def __iter__(self):
        return _lookup_table_item_choice_iterator(self.lookuptable)


class LookupTableItemField(db_models.Field):

    def __init__(self, table_ref, *args, **kwargs):
        self.lookuptable = models.LookupTable.objects.filter(table_ref=table_ref).first()
        if not self.lookuptable:
            self.lookuptable = models.LookupTable.objects.create(table_ref=table_ref, name=table_ref)
        super(LookupTableItemField, self).__init__(*args, **kwargs)
