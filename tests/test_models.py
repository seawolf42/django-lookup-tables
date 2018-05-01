from django.db import IntegrityError
from django.test import TestCase

from lookup_tables import models


strings = [x * 3 for x in range(3)]


class LookupTableTest(TestCase):

    def setUp(self):
        self.item = models.LookupTable.objects.create(name=strings[0])

    def test_fields_exist(self):
        pass

    def test_names_must_be_unique(self):
        models.LookupTable.objects.create(name=strings[1])
        with self.assertRaises(IntegrityError):
            models.LookupTable.objects.create(name=self.item.name)


class LookupTableItemTest(TestCase):

    def setUp(self):
        self.table = models.LookupTable.objects.create(name=strings[-1])
        self.item = models.LookupTableItem.objects.create(name=strings[0], table=self.table)

    def test_fields_exist(self):
        self.assertIsNotNone(self.item.sort_order)

    def test_table_is_mandatory(self):
        self.item.table = None
        self.assertRaises(IntegrityError, self.item.save)

    def test_table_relationship(self):
        self.assertRaises(IntegrityError, self.table.delete)

    def test_names_must_be_unique_per_table(self):
        models.LookupTableItem.objects.create(name=strings[1], table=self.table)
        with self.assertRaises(IntegrityError):
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
