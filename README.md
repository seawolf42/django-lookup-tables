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

In the admin you will see an entry for 'Lookup Tables'. Here you can add tables.

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

I am actively seeking contributions to this package. Things that need to be completed for it to be usable generally:

* Simple way to reference lookup values
* Simple way to reference lookup tables
* REST API (using Django Rest Framework) for looking up all the value options for a foreign key

If you have suggestions for other features I am open to hearing them. Use the "Issues" section of the repository to start a conversation.
