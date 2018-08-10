from django.apps import apps
from django.db import models as db_models


class LookupField(db_models.ForeignKey):

    def __init__(self, to, *args, **kwargs):
        self.table = to
        self._is_initialized = False
        kwargs['to'] = to
        kwargs['on_delete'] = db_models.PROTECT
        kwargs['limit_choices_to'] = self.get_lookup_choices
        kwargs['default'] = self.get_default_lookup
        kwargs['related_name'] = '+'
        super(LookupField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(LookupField, self).deconstruct()
        if 'limit_choices_to' in kwargs:
            del kwargs['limit_choices_to']
        if 'default' in kwargs:
            del kwargs['default']
        return name, path, args, kwargs

    def get_lookup_choices(self):
        return db_models.Q()

    def get_default_lookup(self):
        if not apps.ready:
            return None
        return None
        # return self.table.objects.filter(is_default=True).first()


class LookupTableItemField(db_models.ForeignKey):

    def __init__(self, *args, **kwargs):
        raise Exception('this class is no longer supported; see Betas.md for upgrade information')
