from django.core.management import call_command

from ...fields import get_one_to_many_fields
from ...fields import get_self_reference_fields
from ... import models

from ._base_dumper import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Load data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--babel', '-b',
            dest='babel',
            action='store_true',
            default=False,
            help='Load babel data.')

    def handle(self, **options):
        self.verbosity = options['verbosity']

        self.load_all()

        for field in get_self_reference_fields(models.Country):
            self.load_country_self_reference(field.name)

        if options['babel']:
            models.Locale.objects.load_babel_data()

    def loaddata(self, fixture_path):
        if not self.is_excluded(fixture_path):
            call_command('loaddata', fixture_path, verbosity=self.verbosity)

    def load_all(self):
        one_to_many_fields = [
            field.name for field in get_one_to_many_fields(models.Country)
        ]

        for fixture_path in sorted(
                self.get_fixtures(),
                key=lambda path: any(f in path for f in one_to_many_fields)):

            self.loaddata(fixture_path)

    def load_country_self_reference(self, name):
        with self.open_fixture("self/{}".format(name), 'r') as fixture:
            for data in fixture.read():
                country = models.Country.objects.get(cca2=data.object.pk)
                getattr(country, name).add(*data.m2m_data[name])
