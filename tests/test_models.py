import sys

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import models as db_models
from django.test import TestCase

from lookup_tables import models

from . import utils

if sys.version_info[0] < 3:
    # python 2
    import mock
else:
    # python 3
    from unittest import mock


strings = utils.strings


class ModelTestMixin(object):

    def _test_base_properties(self, name, type, null=False, blank=False, unique=False, editable=True):
        field = self.item._meta.get_field(name)
        self.assertIsInstance(field, type)
        self.assertEqual(field.null, null)
        self.assertEqual(field.blank, blank)
        self.assertEqual(field.unique, unique)
        self.assertEqual(field.editable, editable)
        return field

    def _test_save_calls_full_clean(self, mock_save):
        self.item.full_clean = mock.MagicMock()
        self.item.save()
        self.item.full_clean.assert_called_once()


class LookupTableTest(ModelTestMixin, TestCase):

    def setUp(self):
        self.item = models.LookupTable()

    def test_table_ref_properties(self):
        field = self._test_base_properties('table_ref', db_models.CharField, unique=True, editable=False)
        self.assertEqual(field.max_length, 100)

    def test_name_properties(self):
        field = self._test_base_properties('name', db_models.CharField, unique=True)
        self.assertEqual(field.max_length, 100)

    @mock.patch('django.db.models.Model.save')
    def test_save_calls_full_clean(self, mock_save):
        self._test_save_calls_full_clean(mock_save)

    def test_full_clean_cleans_necessary_fields(self):
        self.item._clean_table_ref = mock.MagicMock()
        self.item.clean()
        self.item._clean_table_ref.assert_called_once()

    def test_clean_table_ref(self):
        self.item.name = 'A Regular String'
        self.item._clean_table_ref()
        self.assertEqual(self.item.table_ref, 'a-regular-string')


class LookupTableItemTest(ModelTestMixin, TestCase):

    def setUp(self):
        self.table = models.LookupTable.objects.create(table_ref=strings[-1], name=strings[-1])
        self.item = models.LookupTableItem.objects.create(name=strings[0], table=self.table)

    def test_table_properties(self):
        field = self._test_base_properties('table', db_models.ForeignKey, editable=False)
        self.assertEqual(field.related_model, models.LookupTable)
        self.assertEqual(field.remote_field.on_delete, db_models.PROTECT)

    def test_name_properties(self):
        field = self._test_base_properties('name', db_models.CharField)
        self.assertEqual(field.max_length, 100)

    def test_sort_order_properties(self):
        field = self._test_base_properties('sort_order', db_models.PositiveSmallIntegerField)
        self.assertEqual(field.default, 0)

    def test_table_relationship(self):
        self.assertRaises(IntegrityError, self.table.delete)

    def test_names_must_be_unique_per_table(self):
        models.LookupTableItem.objects.create(name=strings[1], table=self.table)
        with self.assertRaises(ValidationError):
            models.LookupTableItem.objects.create(name=self.item.name, table=self.table)

    def test_names_can_be_same_in_different_table(self):
        table2 = models.LookupTable.objects.create(name=strings[-2])
        models.LookupTableItem.objects.create(name=self.item.name, table=table2)

    def test_ordering(self):
        self.item.sort_order = 3
        self.item.save()
        item2 = models.LookupTableItem.objects.create(name=strings[-1], table=self.table, sort_order=1)
        item3 = models.LookupTableItem.objects.create(name=strings[-2], table=self.table, sort_order=4)
        table2 = models.LookupTable.objects.create(name=strings[-2])
        item4 = models.LookupTableItem.objects.create(name=strings[-1], table=table2, sort_order=2)
        self.assertEquals(
            list(models.LookupTableItem.objects.all()),
            [item2, item4, self.item, item3]
        )

    @mock.patch('django.db.models.Model.save')
    def test_save_calls_full_clean(self, mock_save):
        self._test_save_calls_full_clean(mock_save)

    def test_full_clean_cleans_necessary_fields(self):
        self.item._clean_table = mock.MagicMock()
        self.item.clean()
        self.item._clean_table.assert_called_once()

    def test_table_cannot_change_on_existing_item(self):
        self.item.table = models.LookupTable.objects.create(name=strings[-2])
        with self.assertRaises(ValidationError):
            self.item._clean_table()
