import os
import sys

from django.core.management import execute_from_command_line


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    os.environ.setdefault('LOOKUP_TABLES_DRF_FIELD_INIT_NO_RESET', str(sys.argv[1] != 'runserver'))
    execute_from_command_line(sys.argv)
