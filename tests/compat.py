"""
The `compat` module provides support for backwards compatibility with older
versions of Django/Python, and compatibility wrappers around optional packages.
"""
import django

try:
    from django.urls import reverse
except ImportError:  # Django < 1.10
    from django.core.urlresolvers import reverse


def get_postgres_engine():
    if django.VERSION >= (2, 0):
        return 'django.db.backends.postgresql'
    return 'django.contrib.gis.db.backends.postgis'
