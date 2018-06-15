from rest_framework import viewsets

from . import models
from . import serializers


class MyModelViewSet(viewsets.ModelViewSet):

    model = models.MyModel
    serializer_class = serializers.MyModelSerializer
    queryset = models.MyModel.objects.all()
