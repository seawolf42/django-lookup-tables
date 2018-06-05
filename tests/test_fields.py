from django.db import models as db_models
from django.test import TestCase

from lookup_tables import fields
from lookup_tables import models

from . import utils


strings = utils.strings


class TestLookupTableItemChoicesIterators(TestCase):

    def setUp(self):
        self.table = models.LookupTable.objects.create(table_ref=strings[0], name=strings[0])
        self.values = [
            models.LookupTableItem.objects.create(table=self.table, name=strings[i], sort_order=i)
            for i in range(len(strings) - 1)
        ]

    def test_iterator(self):
        iterator = fields._lookup_table_item_choice_iterator(self.table)
        for i, choice in enumerate(iterator):
            self.assertEqual(choice[0], self.values[i].pk)
            self.assertEqual(choice[1], self.values[i].name)

    def test_iterator_only_loads_items_from_selected_table(self):
        table2 = models.LookupTable.objects.create(table_ref=strings[-1], name=strings[-1])
        models.LookupTableItem.objects.create(table=table2, name=strings[0], sort_order=0)
        iterator = fields._lookup_table_item_choice_iterator(self.table)
        for i, choice in enumerate(iterator):
            self.assertEqual(choice[0], self.values[i].pk)
            self.assertEqual(choice[1], self.values[i].name)

    def test_wrapper(self):
        iterator = fields._lookup_table_item_choices(self.table)
        for i, choice in enumerate(iterator):
            self.assertEqual(choice[0], self.values[i].pk)
            self.assertEqual(choice[1], self.values[i].name)

    def test_wrapper_lazy_loads(self):
        iterator = fields._lookup_table_item_choices(self.table)
        self.values.append(
            models.LookupTableItem.objects.create(table=self.table, name=strings[-1], sort_order=len(strings))
        )
        for i, choice in enumerate(iterator):
            self.assertEqual(choice[0], self.values[i].pk)
            self.assertEqual(choice[1], self.values[i].name)

    def test_iterator_honors_sort_order(self):
        for i, value in enumerate(self.values):
            value.sort_order = len(strings) - i
            value.save()
        self.values.reverse()
        iterator = fields._lookup_table_item_choices(self.table)
        for i, choice in enumerate(iterator):
            self.assertEqual(choice[0], self.values[i].pk)
            self.assertEqual(choice[1], self.values[i].name)


class TestLookupTableItemFieldCreation(TestCase):

    def test_table_created_from_field_reference(self):
        class DummyFieldTestModel(db_models.Model):
            lookup = fields.LookupTableItemField(table_ref=strings[0])

            class Meta:
                app_label = 'test'

        self.table = models.LookupTable.objects.get(table_ref=strings[0])
        self.assertEqual(models.LookupTable.objects.count(), 1)
