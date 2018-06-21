from django.apps import apps
from django.db import models as db_models

from . import conf
from . import models


_IGNORE_FIELD_DEFAULT_LOOKUPS = conf.IS_RUNNING_MANAGEMENT


class LookupTableItemField(db_models.ForeignKey):

    def __init__(self, table_ref, *args, **kwargs):
        self.table_ref = table_ref
        self._is_initialized = False
        kwargs['to'] = 'lookup_tables.LookupTableItem'
        kwargs['on_delete'] = db_models.PROTECT
        kwargs['limit_choices_to'] = self.get_lookuptableitem_choices
        kwargs['default'] = self.get_default_lookuptableitem
        kwargs['related_name'] = '+'
        super(LookupTableItemField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(LookupTableItemField, self).deconstruct()
        if 'limit_choices_to' in kwargs:
            del kwargs['limit_choices_to']
        if 'default' in kwargs:
            del kwargs['default']
        kwargs['table_ref'] = self.table_ref
        return name, path, args, kwargs

    def get_lookuptableitem_choices(self):
        if not self._is_initialized:
            self._init_lookuptable()
        return db_models.Q(table__table_ref=self.table_ref)

    def get_default_lookuptableitem(self):
        if _IGNORE_FIELD_DEFAULT_LOOKUPS or not apps.ready:
            return None
        if not self._is_initialized:
            self._init_lookuptable()
        return models.LookupTableItem.objects.filter(table__table_ref=self.table_ref, is_default=True).first()

    def _init_lookuptable(self):
        lookuptable = models.LookupTable.objects.filter(table_ref=self.table_ref).first()
        if not lookuptable:
            lookuptable = models.LookupTable.objects.create(table_ref=self.table_ref, name=self.table_ref)
            models.LookupTableItem.objects.create(table=lookuptable, name='<DEFAULT>')
        self._is_initialized = True
