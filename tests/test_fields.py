import sys

from django.db import models as db_models
from django.test import TestCase

from lookup_tables import fields
from lookup_tables import models

from . import utils

if sys.version_info[0] < 3:
    # python 2
    import mock
else:
    # python 3
    from unittest import mock


strings = utils.strings


class LookupTableItemField(TestCase):

    @mock.patch('django.db.models.ForeignKey.__init__')
    def test_construction(self, mock_fk_init):
        self.assertEqual(models.LookupTable.objects.filter(name=strings[0]).count(), 0)
        item = fields.LookupTableItemField(table_ref=strings[0])
        self.assertEqual(models.LookupTable.objects.filter(name=strings[0]).count(), 1)
        self.assertEqual(item.table_ref, strings[0])
        self.assertEqual(item.lookuptable, models.LookupTable.objects.get())

    @mock.patch('django.db.models.ForeignKey.__init__')
    def test_kwargs_includes_foreign_key_requisite_values(self, mock_fk_init):
        item = fields.LookupTableItemField(table_ref=strings[0])
        mock_fk_init.assert_called_once_with(
            to='lookup_tables.LookupTableItem',
            on_delete=db_models.PROTECT,
            limit_choices_to=item.get_lookuptableitem_choices,
        )

    @mock.patch('django.db.models.ForeignKey.__init__')
    def test_get_lookuptable_choices_returns_q_object(self, mock_fk_init):
        item = fields.LookupTableItemField(table_ref=strings[0])
        self.assertIsInstance(item.get_lookuptableitem_choices(), db_models.Q)

    def test_deconstruct_removes_programmatic_args(self):
        item = fields.LookupTableItemField(table_ref=strings[0])
        name, path, args, kwargs = item.deconstruct()
        self.assertTrue('to' in kwargs)
        self.assertTrue('on_delete' in kwargs)
        self.assertFalse('limit_choices_to' in kwargs)
        self.assertEqual(kwargs['table_ref'], strings[0])

    def test_get_choices(self):
        item = fields.LookupTableItemField(table_ref=strings[0])
        table = models.LookupTable.objects.get(name=strings[0])
        choices = [
            models.LookupTableItem.objects.create(table=table, name=strings[i], sort_order=i)
            for i in range(len(strings))
        ]
        models.LookupTableItem.objects.create(
            table=models.LookupTable.objects.create(name=strings[-1]),
            name=strings[-1]
        )
        q_filter = item.get_lookuptableitem_choices()
        for i, choice in enumerate(models.LookupTableItem.objects.filter(q_filter)):
            self.assertEqual(choice, choices[i])


class TestLookupTableItemFieldCreation(TestCase):

    def test_table_created_from_field_reference(self):
        class DummyFieldTestModel(db_models.Model):
            lookup = fields.LookupTableItemField(table_ref=strings[0])

            class Meta:
                app_label = 'test'

        self.table = models.LookupTable.objects.get(table_ref=strings[0])
        self.assertEqual(models.LookupTable.objects.count(), 1)
