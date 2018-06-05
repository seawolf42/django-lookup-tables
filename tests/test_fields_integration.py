from django.db import models as db_models
from django.test import TestCase

from lookup_tables import fields
from lookup_tables import models


strings = [x * 3 for x in 'abc']


class TestLookupTableItemField(TestCase):

    def _get_model(self):
        class DummyModel(db_models.Model):
            lookup = fields.LookupTableItemField(table_ref=strings[0])

            class Meta:
                app_label = 'test'

        return DummyModel

    def setUp(self):
        self.model = self._get_model()

    def test_table_created_from_field_reference(self):
        self.assertEqual(models.LookupTable.objects.count(), 1)
