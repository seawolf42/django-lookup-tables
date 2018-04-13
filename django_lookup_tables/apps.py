from django.apps import AppConfig


class Config(AppConfig):
    name = 'django_lookup_tables'
    verbose_name = 'Lookup Tables'

    def ready(self):
        pass
