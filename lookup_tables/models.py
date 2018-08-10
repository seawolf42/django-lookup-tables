from django.db import models
from django.db import transaction


class AbstractLookupTable(models.Model):

    name = models.CharField(max_length=100, unique=True)

    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ('sort_order',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            super(AbstractLookupTable, self).save(*args, **kwargs)


class LookupTable(models.Model):

    def __init__(self, *args, **kwargs):
        raise Exception('this class is no longer supported; see Betas.md for upgrade information')


class LookupTableItem(models.Model):

    def __init__(self, *args, **kwargs):
        raise Exception('this class is no longer supported; see Betas.md for upgrade information')
