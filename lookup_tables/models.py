from django.core.exceptions import ValidationError
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

    def _clean_table(self):
        if not self.id:
            return
        previous = LookupTableItem.objects.get(pk=self.pk)
        if previous.table != self.table:
            raise ValidationError('cannot change table name on existing lookup values')

    def clean(self):
        self._clean_table()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(LookupTableItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
