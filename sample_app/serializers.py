from rest_framework import serializers

from lookup_tables.drf_fields import LookupSerializerField

from . import models


class MyModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.MyModel
        fields = ('url', 'name', 'type', 'status', 'category')
        extra_kwargs = {'url': {'view_name': 'api:mymodel-detail'}}

    type = LookupSerializerField(models.MyModelType, required=False)
    status = LookupSerializerField(models.MyModelStatus)
    category = LookupSerializerField(models.MyModelCategory, required=False, allow_null=True)
