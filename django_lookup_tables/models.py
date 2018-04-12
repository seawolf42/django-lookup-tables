from django.db import models


class LookupTable(models.Model):

    name = models.CharField(max_length=100)
