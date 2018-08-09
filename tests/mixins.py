from django.test import TestCase
from django.db import connection
from django.db.models.base import ModelBase


# copied/adapted from https://stackoverflow.com/a/45239964


class ModelMixinTestCase(TestCase):
    '''
    Base class for tests of model mixins. To use, subclass and specify the
    mixin class variable. A model using the mixin will be made available in
    self.model
    '''

    @classmethod
    def setUpClass(cls):
        cls.model = ModelBase(
            cls.__name__ + cls.mixin.__name__,
            (cls.mixin,),
            {'__module__': cls.mixin.__module__},
        )
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls.model)
        super(ModelMixinTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(cls.model)
        super(ModelMixinTestCase, cls).tearDownClass()
