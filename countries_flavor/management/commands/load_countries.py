import os

from django.core.management import call_command

from ... import models
from ._base_dumper import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Load fixtures'

    def handle(self, **options):
        fixtures = []

        for root, dirs, files in os.walk(self.rootdir, topdown=True):
            if 'm2m' in dirs:
                dirs.remove('m2m')

            for fixture in files:
                fixtures.append(os.path.join(
                    root.split('fixtures/')[1], fixture))

        for fixture in sorted(fixtures, key=lambda path: any(
                f in path for f in ('all/locale', 'divisions', 'names'))):
            call_command('loaddata', fixture)

        with self.open_fixture('m2m/borders', 'r') as fixture:
            for data in fixture.read():
                country = models.Country.objects.get(cca2=data.object.pk)
                country.borders.add(*data.m2m_data['borders'])
