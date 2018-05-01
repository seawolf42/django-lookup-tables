from django.apps import AppConfig


class Config(AppConfig):
    name = 'lookup_tables'
    verbose_name = 'Lookup Tables'

    def ready(self):
        pass
