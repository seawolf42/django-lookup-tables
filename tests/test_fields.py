import sys

from django.db import models as db_models

from lookup_tables import fields
from lookup_tables import models

from . import mixins
from . import utils

if sys.version_info[0] < 3:
    # python 2
    import mock
else:
    # python 3
    from unittest import mock


strings = utils.strings


class LookupField(mixins.ModelMixinTestCase):

    mixin = models.AbstractLookupTable

    @mock.patch('django.db.models.ForeignKey.__init__')
    def test_construction(self, mock_fk_init):
        item = fields.LookupField(to=self.model)
        self.assertEqual(item.table, self.model)
        self.assertEqual(item._is_initialized, False)

    @mock.patch('django.db.models.ForeignKey.__init__')
    def test_kwargs_includes_foreign_key_requisite_values(self, mock_fk_init):
        item = fields.LookupField(to=self.model)
        mock_fk_init.assert_called_once_with(
            to=self.model,
            on_delete=db_models.PROTECT,
            limit_choices_to=item.get_lookup_choices,
            default=item.get_default_lookup,
            related_name='+',
        )

    @mock.patch('django.db.models.ForeignKey.__init__')
    def test_get_lookup_choices_returns_q_object(self, mock_fk_init):
        item = fields.LookupField(to=self.model)
        self.assertIsInstance(item.get_lookup_choices(), db_models.Q)

    def test_deconstruct_removes_programmatic_args(self):
        item = fields.LookupField(to=self.model)
        name, path, args, kwargs = item.deconstruct()
        self.assertTrue('to' in kwargs)
        self.assertTrue('on_delete' in kwargs)
        self.assertFalse('limit_choices_to' in kwargs)
        self.assertFalse('default' in kwargs)

    def test_get_choices(self):
        item = fields.LookupField(to=self.model)
        choices = [
            self.model.objects.create(name=strings[i], sort_order=i)
            for i in range(len(strings))
        ]
        q_filter = item.get_lookup_choices()
        for i, choice in enumerate(self.model.objects.filter(q_filter)):
            self.assertEqual(choice, choices[i])
