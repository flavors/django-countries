#!/usr/bin/env python

import os
import sys

import django

from django.conf import settings
from django.test.runner import DiscoverRunner

from tests.compat import get_postgres_engine


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django_filters',
        'rest_framework',
        'rest_framework_gis',
        'countries_flavor.apps.CountriesAppConfig',
        'tests'
    ),
    DATABASES={
        'default': {
            'ENGINE': get_postgres_engine(),
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', '')
        }
    },
    ROOT_URLCONF='tests.urls',
    REST_FRAMEWORK={
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework_filters.backends.DjangoFilterBackend',
            'rest_framework.filters.OrderingFilter',
            'rest_framework.filters.SearchFilter'
        ),
        'TEST_REQUEST_DEFAULT_FORMAT': 'json'
    }
)


def runtests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    failures = DiscoverRunner(
        verbosity=1,
        interactive=True,
        failfast=False)\
        .run_tests(['tests'])

    sys.exit(failures)


if __name__ == '__main__':
    runtests()
