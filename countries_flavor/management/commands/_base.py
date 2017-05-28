from pathlib import Path

from django.core import serializers
from django.core.management.base import BaseCommand


__all__ = ['DumperBaseCommand']


class TextIOWrapper(object):

    def __init__(self, path, mode, format, is_fake=False):
        self.format = format
        self.is_fake = is_fake

        if not is_fake:
            self._file = open(path.as_posix(), mode)
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
        self._rootdir = Path(__file__).parents[2] / 'fixtures'
        super().__init__(*args, **kwargs)

    def get_fixture_path(self, path):
        path = Path(path)
        if not path.is_absolute():
            return self._rootdir / path.with_name(path.name + '.json')
        return path

    def get_country_path(self, country, name):
        return Path('countries', country.cca2.lower()).with_suffix('.' + name)

    def open_fixture(self, path, mode):
        path = self.get_fixture_path(path)

        return TextIOWrapper(
            path=path,
            mode=mode,
            format='json',
            is_fake=self.is_excluded(path)
        )

    def is_excluded(self, path):
        return next((
            True for pattern in self.exclude_fixtures
            if path.match(pattern)), False
        )
