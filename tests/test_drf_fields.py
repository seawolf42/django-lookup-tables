import sys

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from lookup_tables.drf_fields import LookupTableItemSerializerField

from .utils import strings

if sys.version_info[0] < 3:
    # python 2
    import mock
else:
    # python 3
    from unittest import mock


class MockLTI(object):

    def __init__(self, id):
        self.id = id
        self.name = str(id)


class LookupTableItemSerializerFieldTest(TestCase):

    @mock.patch('rest_framework.fields.ChoiceField.__init__')
    @mock.patch('lookup_tables.drf_fields.LookupTableItemSerializerField._reset_choices')
    def test_init(self, mock_reset_choices, mock_parent_init):
        item = LookupTableItemSerializerField(strings[0], x=strings[-1], y=strings[-2])
        mock_parent_init.assert_called_once_with([], x=strings[-1], y=strings[-2])
        mock_reset_choices.assert_called_once_with()
        self.assertEqual(item._table_ref, strings[0])
        self.assertEqual(item.choices, None)

    @mock.patch('rest_framework.fields.ChoiceField.__init__')
    @mock.patch('lookup_tables.drf_fields.LookupTableItemSerializerField._reset_choices')
    @mock.patch('lookup_tables.drf_fields._IGNORE_INIT_RESET')
    def test_init_no_reset(self, mock_ignore_reset_setting, mock_reset_choices, mock_parent_init):
        item = LookupTableItemSerializerField(strings[0], x=strings[-1], y=strings[-2])
        mock_parent_init.assert_called_once_with([], x=strings[-1], y=strings[-2])
        mock_reset_choices.assert_not_called()
        self.assertEqual(item._table_ref, strings[0])
        self.assertEqual(item.choices, None)

    def test_to_internal_value_handles_empty_reply(self):
        item = LookupTableItemSerializerField(strings[0], allow_blank=True)
        self.assertIsNone(item.to_internal_value(''))

    @mock.patch('lookup_tables.drf_fields.LookupTableItem')
    def test_to_internal_value_sets_choices(self, mock_lti):
        lti_get_return_value = mock.MagicMock()
        mock_lti.objects.get.return_value = lti_get_return_value
        lti_filter_return_value = [MockLTI(i) for i in range(3)]
        mock_lti.objects.filter.return_value = lti_filter_return_value
        item = LookupTableItemSerializerField(strings[0])
        result = item.to_internal_value('1')
        self.assertEqual(result, lti_get_return_value)
        mock_lti.objects.get.assert_called_once_with(table__table_ref=item._table_ref, id=1)

    @mock.patch('lookup_tables.drf_fields.LookupTableItem')
    def test_to_internal_value_invalid_value(self, mock_lti):
        mock_lti.objects.filter.return_value = [MockLTI(i) for i in range(3)]
        mock_lti.DoesNotExist = Exception
        item = LookupTableItemSerializerField(strings[0])
        with self.assertRaises(ValidationError):
            item.to_internal_value('1000')

    @mock.patch('lookup_tables.drf_fields.LookupTableItem')
    def test_to_internal_value_invalid_table_id(self, mock_lti):
        mock_lti.objects.filter.return_value = [MockLTI(i) for i in range(3)]
        mock_lti.DoesNotExist = Exception
        mock_lti.objects.get.side_effect = Exception
        item = LookupTableItemSerializerField(strings[0])
        with self.assertRaises(ValidationError):
            item.to_internal_value('1')

    def test_to_representation(self):
        item = LookupTableItemSerializerField(strings[0])
        self.assertEqual(item.to_representation(MockLTI(1)), 1)

    @mock.patch('lookup_tables.drf_fields._REPR_NAME')
    def test_to_representation_name_not_id(self, mock_repr_setting):
        mock_repr_setting.return_value = True
        item = LookupTableItemSerializerField(strings[0])
        self.assertEqual(item.to_representation(MockLTI(1)), '1')

    @mock.patch('lookup_tables.drf_fields.LookupTableItemSerializerField._get_choices')
    @mock.patch('lookup_tables.drf_fields.LookupTableItemSerializerField._set_choices')
    def test_reset_choices(self, mock_set_choices, mock_get_choices):
        mock_get_choices.return_value = []
        item = LookupTableItemSerializerField(strings[0])
        item._choices = strings[0]
        mock_get_choices.return_value = strings[1]
        mock_get_choices.reset_mock()
        mock_set_choices.reset_mock()
        item._reset_choices()
        self.assertEqual(item._choices, None)
        mock_get_choices.assert_called_once_with()
        mock_set_choices.assert_called_once_with(strings[1])
