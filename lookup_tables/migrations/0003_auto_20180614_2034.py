# Generated by Django 2.0.4 on 2018-06-15 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lookup_tables', '0002_table_ref_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='lookuptable',
            name='default',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lookup_tables.LookupTableItem'),
        ),
        migrations.AddField(
            model_name='lookuptableitem',
            name='is_default',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
