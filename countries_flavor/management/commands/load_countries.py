import os

from django.core.management import call_command

from ...fields import get_one_to_many_fields
from ...fields import get_self_reference_fields
from ... import models

from ._base_dumper import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Load fixtures'

    def handle(self, **options):
        fixtures = []

        for root, dirs, files in os.walk(self._rootdir, topdown=True):
            if 'self' in dirs:
                dirs.remove('self')

            for fixture in files:
                fixtures.append(os.path.join(
                    root.split('fixtures/')[1], fixture))

        self.loaddata(fixtures)

        for field in get_self_reference_fields(models.Country):
            self.load_country_self_reference(field.name)

    @classmethod
    def loaddata(self, fixtures):
        one_to_many_fields = [
            field.name for field in get_one_to_many_fields(models.Country)
        ]

        for fixture in sorted(fixtures, key=lambda path: any(
                field in path for field in one_to_many_fields)):

            call_command('loaddata', fixture)

    def load_country_self_reference(self, name):
        with self.open_fixture("self/{}".format(name), 'r') as fixture:
            for data in fixture.read():
                country = models.Country.objects.get(cca2=data.object.pk)
                getattr(country, name).add(*data.m2m_data[name])
