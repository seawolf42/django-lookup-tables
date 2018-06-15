from rest_framework import serializers

from lookup_tables.drf_fields import LookupTableItemSerializerField

from . import models


class MyModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.MyModel
        fields = ('url', 'name', 'type', 'status', 'category')
        extra_kwargs = {'url': {'view_name': 'api:mymodel-detail'}}

    type = LookupTableItemSerializerField(table_ref='mymodel-type', required=False)
    status = LookupTableItemSerializerField(table_ref='mymodel-status')
    category = LookupTableItemSerializerField(table_ref='mymodel-category', required=False, allow_null=True)
