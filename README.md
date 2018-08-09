# Django Lookup Tables

Efficient storage and management of lookup tables used throughout an app.

**Note:** This package is a work in progress (that's why it's not yet at version 1.0). I am active seeking contributions to help with making it more usable, see ["Contributing"](#contributing) below.


# IMPORTANT

This software is still pre-release. Upgrades from one version to the next may create unstabilities in your project. If you have used any version prior to `1.0.0`, please read the [Release Notes for Beta Versions](docs/Betas.md).


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
from lookup_tables.models import AbsractLookupTable
from lookup_tables.fields import LookupField

class PostState(AbstractLookupTable):
    pass

class Post(models.Model):
    title = models.CharField(max_length=100)
    state = LookupField(PostState)
```

This will create a lookup table called `PostState` that can be administered by staff users. You can now set this field to any value from the `PostState` model.

If you register your model in the app's `admin.py`:

```python
from django.contrib import admin
from lookup_tables.admin import LookupAdmin
from .models import PostState

@admin.register(PostState)
class PostStateAdmin(LookupAdmin):
    pass

```

... you will be able to modify the values in the table through the "Post State" link in the Django admin.

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

Fields on models will render the same way `CharField` does if you use the `drf_fields.LookupSerializerField` field on your serializer like so:

```python
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'state')

    state = LookupSerializerField(PostState)
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
