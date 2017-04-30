import os
import re

from django.core import serializers
from django.core.management.base import BaseCommand


class TextIOWrapper(object):

    def __init__(self, path, mode, format, is_fake=False):
        self.format = format
        self.is_fake = is_fake

        if not is_fake:
            self._file = open(path, mode)
        else:
            self._file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.is_fake:
            self._file.close()

    def read(self):
        if self.is_fake:
            return list()
        return serializers.deserialize(self.format, self._file.read())

    def write(self, queryset, **kwargs):
        if not self.is_fake:
            data = serializers.serialize(self.format, queryset, **kwargs)
            self._file.write(data)


class DumperBaseCommand(BaseCommand):
    exclude_fixtures = tuple()

    def __init__(self, *args, **kwargs):
        self._rootdir = os.path.abspath(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), os.pardir, 'fixtures'))

        self._exclude_patterns =\
            list(map(re.compile, list(self.exclude_fixtures)))

        super(DumperBaseCommand, self).__init__(*args, **kwargs)

    def get_fixtures(self):
        fixtures = []

        for root, dirs, files in os.walk(self._rootdir, topdown=True):
            # Exclude self references
            if 'self' in dirs:
                dirs.remove('self')

            for fixture in files:
                fixtures.append(os.path.join(
                    root.split('fixtures/')[1], fixture))
        return fixtures

    def get_fixture_path(self, path):
        return "{path}.json".format(path=os.path.join(self._rootdir, path))

    def get_country_path(self, country, name):
        return "countries/{cca2}.{name}".format(
            cca2=country.cca2.lower(),
            name=name)

    def open_fixture(self, path, mode):
        return TextIOWrapper(
            self.get_fixture_path(path),
            mode=mode,
            format='json',
            is_fake=self.is_excluded(path))

    def is_excluded(self, path):
        return next((
            True for pattern in self._exclude_patterns
            if pattern.match(path)), False
        )
