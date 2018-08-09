# Release Notes for Beta Versions

## Pre Version 0.14:

Versions `0.1` through `0.13` implemented lookup tables using the [One True Lookup Table](https://www.apress.com/gp/blog/all-blog-posts/best-practices-for-using-simple-lookup-tables/13323426) anti-pattern. If you have used this project in its earlier versions, please upgrade in the following way:

### Steps

1. Upgrade to version `0.14` (ONLY to this specific version, it has the helpers necessary to transfer data to the new structure)
1. Create a replacement lookup table class that inherits from `models.AbstractLookupTable`
1. Create new fields mirroring the existing `LookupTableItemField`s on your model, with `_new` appended to the field name, remove the `table_ref` arg, and make the first (unnamed) argument a reference to the concrete lookup table class
1. Run `./manage.py makemigrations`
1. Open the migration and add a call to `utils.migration_helpers.copy_data` as shown below
1. Delete the old fields
1. Run `./manage.py makemigrations`
1. Open the migration and add a call to `utils.migration_helpers.delete_data` as shown below
1. Rename the new fields to the desired field names
1. Run `./manage.py makemigrations`
1. Change any `LookupTableItemSerializerField`s to `LookupSerializerField`, remove the `table_ref` kwarg, and make the first (unnamed) argument a reference to the concrete lookup table class

If desired, you can combine those migrations into a single migration, but it will be much easier to have the `makemigrations` tool build most of it for you.

### Example

After the new fields are created and before the old fields are deleted, you will want to populate the new lookup table with the values from the previous lookup table and copy the field values into the newly-created field. This can be accomplished as follows:

Open the correct migration file (the one that adds the new tables and creates the `x_new` fields as described above), and in the right point in the sequence of migrations, add a call to `copy_data`: `migrations.RunPython(copy_data),`. Then create a method at the top of the file like this:

```python
# migration file header as auto-generated

from lookup_tables.utils import migration_helpers

LOOKUP_FIELD_CHANGES = (
    ('my-lookup-table-1-ref', 'MyModel', 'MyLookupTableModel1', 'model_field_1_name'),
    ('my-lookup-table-2-ref', 'MyModel', 'MyLookupTableModel2', 'model_field_2_name'),
)

def copy_data(apps, schema_editor):
    migration_helpers.copy_data(apps, schema_editor, 'my_package', LOOKUP_FIELD_CHANGES)

def delete_data(apps, schema_editor):
    migration_helpers.delete_data(apps, schema_editor, 'my_package', LOOKUP_FIELD_CHANGES)

class Migration(migrations.Migration):
    # ...
    operations = [
        # calls to CreateModel
        # calls to AddField
        migrations.RunPython(copy_data),
        # calls to RemoveField
        migrations.RunPython(delete_data),
        # calls to AlterField
    ]
```

The `LOOKUP_FIELD_CHANGES` variable is an iterable of iterables. Each member should contain the following elements:

1. The `table_ref` used to define the original LookupTableItemField
1. The name of the model containing the field being upgraded
1. The name of the concrete lookup table class that inherits from `AbstractLookupTable`
    1. if the lookup table is in a different package/app, give the qualified name for the model in the form `app_name.ModelName`
1. The name of the field being upgraded
    1. f more than one field references the same lookup table, you can combine them as a `,`-delimited list, such as `'field_1,field_2'`.

Once you've removed all references to `LookupTableItemField` and `LookupTableItemSerializerField` you can upgrade to versions > `0.14`.
