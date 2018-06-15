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

This will create a lookup table called "post-state" that has a single option, `'<DEFAULT>'`. You can now set this field to any value from the `LookupTableItems` model that references the `LookupTable.objects.get(table_ref='post-state')` table.

In the admin you will see an entry for 'Lookup Tables'. Here you can manage tables and their associated values. Note that the automatically-generated `'<DEFAULT>'` item can be renamed or removed; this is just created so that the table is not empty on first use.

`django-lookup-tables` integrates properly with forms out of the box, so all UI naturally gets up-to-date selection lists just like if you were using a `CharField` with a choices enum or tuple list.

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


## Using with Django REST Framework

Fields on models will render the same way `CharField` does if you use the `drf_fields.LookupTableItemSerializerField` field on your serializer like so:

```python
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'state')

    state = LookupTableItemSerializerField(table_ref='post-state')
```

By default, the field will send the `id` of the `LookupTableItem`. If you instead want to send the `name` property, add `DRF_REPRESENTATION_NAME_NOT_ID` to your `settings.py`:

```python
LOOKUP_TABLES = {
    # ...
    'DRF_REPRESENTATION_NAME_NOT_ID': True,
    # ...
}
```

The HTML UI provided by DRF will populate dropdowns, and the `OPTIONS` response handler will supply all key/value pairs available for the field:

```json
OPTIONS /api/posts/1/
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "name": "Post Instance",
    "description": "",
    "renders": [
        "application/json",
        "text/html"
    ],
    "parses": [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data"
    ],
    "actions": {
        "PUT": {
            "id": {
                "type": "integer",
                "required": false,
                "read_only": true,
                "label": "ID"
            },
            "title": {
                "type": "string",
                "required": true,
                "read_only": false,
                "label": "Name",
                "max_length": 200
            },
            "state": {
                "type": "choice",
                "required": true,
                "read_only": false,
                "label": "State",
                "choices": [
                    {
                        "value": 14,
                        "display_name": "Draft"
                    },
                    {
                        "value": 18,
                        "display_name": "Published"
                    }
                ]
            }
        }
    }
}
```

**NOTE:** If you are using the `LookupTableItemSerializerField` on any serializer, you need to disable an init hook for all management commands except `runserver`. Failure to do so will result in an error similar to the following:

```bash
django.db.utils.ProgrammingError: relation "lookup_tables_lookuptableitem" does not exist
LINE 1: ..."lookup_tables_lookuptableitem"."sort_order" FROM "lookup_ta...
```

Disabling the init-hook can be controlled by putting the following in your `manage.py` script:

```python
os.environ.setdefault('LOOKUP_TABLES_DRF_FIELD_INIT_NO_RESET', str(sys.argv[1] != 'runserver'))
```

Note additionally that this setting should **not** be disabled in your `wsgi` application.


## Sample App

You can see a sample app using these fields buy running the following:

```bash
$ python manage.py migrate
$ python manage.py loaddata fixtures/base.json
$ python manage.py runserver
```

This app has the following endpoints:

```
/admin/
/api/mymodel/
/api/mymodel/<id>/
```

The username for the admin user is `admin`, and the password is `pass`.


<a name="contributing"></a>
## Contributing

I am actively seeking contributions to this package. Check the "Issues" section of the repository for my current hit list.

If you have suggestions for other features I am open to hearing them. Use the "Issues" section of the repository to start a conversation.
