import unittest

from django_lookup_tables import models


strings = [x * 3 for x in range(3)]


class LookupTableTest(unittest.TestCase):

    def setUp(self):
        self.item = models.LookupTable.objects.create(name=strings[0])

    def test_fields_exist(self):
        self.assertIsNotNone(self.item.name)
