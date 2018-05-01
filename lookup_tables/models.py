from django.db import models


class LookupTable(models.Model):

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Lookup Table'
        ordering = ('name',)

    def __str__(self):
        return self.name


class LookupTableItem(models.Model):

    table = models.ForeignKey(LookupTable, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Lookup Table Item'
        unique_together = ('table', 'name')
        ordering = ('sort_order',)

    def __str__(self):
        return self.name
