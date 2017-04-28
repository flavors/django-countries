import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class DumperBaseCommand(BaseCommand):

    def __init__(self, *args, **kwargs):
        self.rootdir = os.path.abspath(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), os.pardir, 'fixtures'))

        super(DumperBaseCommand, self).__init__(*args, **kwargs)

    @classmethod
    def dumpdata(cls, model_name, path):
        model = "countries_flavor.{model}".format(model=model_name)
        call_command('dumpdata', model, '--output', path)
