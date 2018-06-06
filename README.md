# Django Lookup Tables

Efficient storage and management of lookup tables used throughout an app.

**Note:** This package is a work in progress (that's why it's not yet at version 1.0). I am active seeking contributions to help with making it more usable, see ["Contributing"](#contributing) below.


## Installation

Install the package:

```bash
$ pip install django-lookup-tables
```

Add it to your installed apps:

```python
INSTALLED_APPS = (
    ...
    'lookup_tables',
    ...
)
```


## Usage

The primary use case for lookup tables is to create user-managed lists of options for models to choose from. Consider a model with a field called, for instance, `state`:

```python
from django.db import models
from lookup_tables.fields import LookupTableItemField

CHOICES = (('draft', 'draft'), ('published', 'published'))

class Post(models.Model):
    title = models.CharField(max_length=100)
    state = models.CharField(choices=CHOICES)
```

While this is easy to build, changing the choices list requires rebuilding and redeploying your application.

The above model could instead be written as:

```python
from django.db import models
from lookup_tables.fields import LookupTableItemField

class Post(models.Model):
    title = models.CharField(max_length=100)
    state = LookupTableItemField(table_ref='post-state')
```

This will create a lookup table called "post-state" that has a single option, `'<DEFAULT>'`. You can now set this field to any value from the `LookupTableItems` model that references the `LookupTable.objects.get(table_ref='post_state')` table.

In the admin you will see an entry for 'Lookup Tables'. Here you can manage tables and their associated values. Note that the automatically-generated `'<DEFAULT>'` item can be renamed or removed; this is just created so that the table is not empty on first use.

`django-lookup-tables` integrates properly with forms and `djangorestframework`, so all UI naturally gets up-to-date selection lists just like if you were using a `CharField` with a choices enum or tuple list.

Each table has an arbitrary list of items. You can order them by setting the "Sort Order" field to any positive integer.


## Using with Admin-Sortable2

If you have `django-admin-sortable2` installed, you can take advantage of it's UI enhancements by configuring `django-lookup-tables` to use it. In your `settings.py`:

```python
INSTALLED_APPS = (
    ...
    'adminsortable2',
    'lookup_tables',
    ...
)

LOOKUP_TABLES = {
    'USE_ADMIN_SORTABLE2': True,
}
```


<a name="contributing"></a>
## Contributing

I am actively seeking contributions to this package. Check the "Issues" section of the repository for my current hit list.

If you have suggestions for other features I am open to hearing them. Use the "Issues" section of the repository to start a conversation.
