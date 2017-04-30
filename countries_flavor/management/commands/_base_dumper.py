import os

from django.core import serializers
from django.core.management.base import BaseCommand


class TextIOWrapper(object):

    def __init__(self, path, mode, format):
        self._file = open(path, mode)
        self.format = format

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()

    def read(self):
        return serializers.deserialize(self.format, self._file.read())

    def write(self, queryset, **kwargs):
        data = serializers.serialize(self.format, queryset, **kwargs)
        self._file.write(data)


class DumperBaseCommand(BaseCommand):

    def __init__(self, *args, **kwargs):
        self._rootdir = os.path.abspath(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), os.pardir, 'fixtures'))

        super(DumperBaseCommand, self).__init__(*args, **kwargs)

    def get_fixture_path(self, path):
        return "{path}.json".format(path=os.path.join(self._rootdir, path))

    def open_fixture(self, path, mode):
        return TextIOWrapper(self.get_fixture_path(path), mode, 'json')
