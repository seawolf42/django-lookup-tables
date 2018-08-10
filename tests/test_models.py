import sys

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


class AbstractLookupTableTest(ModelTestMixin, TestCase):

    def setUp(self):
        self.item = models.AbstractLookupTable()

    def test_name_properties(self):
        field = self._test_base_properties('name', db_models.CharField, unique=True)
        self.assertEqual(field.max_length, 100)

    def test_sort_order_properties(self):
        field = self._test_base_properties('sort_order', db_models.PositiveSmallIntegerField)
        self.assertEqual(field.default, 0)

    @mock.patch('django.db.models.Model.save')
    def test_save_calls_full_clean(self, mock_save):
        self._test_save_calls_full_clean(mock_save)
