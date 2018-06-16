from rest_framework import fields
import six

from lookup_tables.models import LookupTableItem

from . import conf


_IGNORE_INIT_RESET = conf.IGNORE_INIT_RESET
_REPR_NAME = conf.DRF_REPRESENTATION_NAME_NOT_ID


class LookupTableItemSerializerField(fields.ChoiceField):

    def __init__(self, table_ref, **kwargs):
        self._table_ref = table_ref
        self._choices = None
        super(LookupTableItemSerializerField, self).__init__([], **kwargs)
        if not _IGNORE_INIT_RESET:
            self._reset_choices()

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return None
        self._reset_choices()
        try:
            return LookupTableItem.objects.get(
                table__table_ref=self._table_ref,
                id=self.choice_strings_to_values[six.text_type(data)],
            )
        except (KeyError, LookupTableItem.DoesNotExist):
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        if value is None:
            return value
        return super(LookupTableItemSerializerField, self).to_representation(value.name if _REPR_NAME else value.id)

    def iter_options(self):
        """
        Helper method for use with templates rendering select widgets.
        """
        self._reset_choices()
        return super(LookupTableItemSerializerField, self).iter_options()

    def _reset_choices(self):
        self._choices = None
        self._set_choices(self._get_choices())

    def _get_choices(self):
        if self._choices is None or len(self._choices) == 0:
            self._choices = [(i.id, i.name) for i in LookupTableItem.objects.filter(table__table_ref=self._table_ref)]
        return self._choices
