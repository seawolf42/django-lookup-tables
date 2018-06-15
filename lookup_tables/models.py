from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction
from django.utils.text import slugify


class LookupTable(models.Model):

    table_ref = models.CharField(max_length=100, unique=True, editable=False)
    name = models.CharField(max_length=100, unique=True)

    default = models.ForeignKey('LookupTableItem', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Lookup Table'
        ordering = ('name',)

    def _clean_table_ref(self):
        if self.table_ref:
            return
        self.table_ref = slugify(self.name)

    def _clean_default(self):
        if self.default and self.default.table != self:
            raise ValidationError('default must be child of this table')

    def clean(self):
        self._clean_table_ref()
        self._clean_default()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            previous_default = LookupTable.objects.get(pk=self.pk).default if self.pk else None
            changed_previous = previous_default != self.default
            if previous_default and changed_previous:
                previous_default.is_default = False
                previous_default.save()
            super(LookupTable, self).save(*args, **kwargs)
            if changed_previous and self.default:
                self.default.is_default = True
                self.default.save()

    def __str__(self):
        return self.name


class LookupTableItem(models.Model):

    table = models.ForeignKey(LookupTable, on_delete=models.PROTECT, editable=False)
    name = models.CharField(max_length=100)

    sort_order = models.PositiveSmallIntegerField(default=0)

    is_default = models.BooleanField(default=False, editable=False)

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

    def _clean_is_default(self):
        if self.is_default:
            # if self.table.default != self:
            #     raise ValidationError('is_default must match table default item')
            if LookupTableItem.objects.filter(table=self.table, is_default=True).exclude(id=self.id).count() > 0:
                raise ValidationError('cannot set is_default on multiple items for the same table')

    def clean(self):
        self._clean_table()
        self._clean_is_default()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            super(LookupTableItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
