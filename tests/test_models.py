import sys

from django.core.exceptions import ValidationError
from django.db import IntegrityError
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


class LookupTableTest(TestCase):

    def setUp(self):
        self.item = models.LookupTable()

    def test_table_ref_properties(self):
        field = self.item._meta.get_field('table_ref')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertTrue(field.unique)
        self.assertFalse(field.editable)
        self.assertEqual(field.max_length, 100)

    def test_name_properties(self):
        field = self.item._meta.get_field('name')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertTrue(field.unique)
        self.assertTrue(field.editable)
        self.assertEqual(field.max_length, 100)

    @mock.patch('django.db.models.Model.save')
    def test_save_calls_full_clean(self, mock_save):
        self.item.full_clean = mock.MagicMock()
        self.item.save()
        self.item.full_clean.assert_called_once()

    def test_full_clean_cleans_necessary_fields(self):
        self.item._clean_table_ref = mock.MagicMock()
        self.item.clean()
        self.item._clean_table_ref.assert_called_once()

    def test_clean_table_ref(self):
        self.item.name = 'A Regular String'
        self.item._clean_table_ref()
        self.assertEqual(self.item.table_ref, 'a-regular-string')


class LookupTableItemTest(TestCase):

    def setUp(self):
        self.table = models.LookupTable.objects.create(table_ref=strings[-1], name=strings[-1])
        self.item = models.LookupTableItem.objects.create(name=strings[0], table=self.table)

    def test_table_properties(self):
        field = self.item._meta.get_field('table')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertFalse(field.editable)

    def test_name_properties(self):
        field = self.item._meta.get_field('name')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertTrue(field.editable)

    def test_sort_order_properties(self):
        field = self.item._meta.get_field('sort_order')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)
        self.assertTrue(field.editable)
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
        self.item.full_clean = mock.MagicMock()
        self.item.save()
        self.item.full_clean.assert_called_once()

    def test_full_clean_cleans_necessary_fields(self):
        self.item._clean_table = mock.MagicMock()
        self.item.clean()
        self.item._clean_table.assert_called_once()

    def test_table_cannot_change_on_existing_item(self):
        self.item.table = models.LookupTable.objects.create(name=strings[-2])
        with self.assertRaises(ValidationError):
            self.item._clean_table()
