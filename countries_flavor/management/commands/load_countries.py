from django.core.management import call_command

from ...fields import get_one_to_many_fields
from ...fields import get_self_reference_fields
from ... import models

from ._base import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Load data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--babel', '-b',
            dest='babel',
            action='store_true',
            default=False,
            help='Load babel data.'
        )

        parser.add_argument(
            '--translations', '-t',
            dest='translations',
            action='store_true',
            default=False,
            help='Load translations data.'
        )

    def handle(self, **options):
        self.verbosity = options['verbosity']

        self.load_all()

        for field in get_self_reference_fields(models.Country):
            self.load_country_self_reference(field.name)

        if options['babel']:
            models.Locale.objects.load_babel(options['translations'])

    def loaddata(self, fixture_path):
        if not self.is_excluded(fixture_path):
            call_command(
                'loaddata',
                fixture_path.as_posix(),
                verbosity=self.verbosity
            )

    def get_fixtures(self, **kwargs):
        return sorted([
            fixture for fixture in self._rootdir.glob('**/*.*')
            if 'self' != fixture.parent.stem
        ], **kwargs)

    def load_all(self):
        one_to_many_fields = [
            field.name for field in get_one_to_many_fields(models.Country)
        ]

        fixtures = self.get_fixtures(
            key=lambda path: any(
                name in path.stem or path.parent.match(name)
                for name in one_to_many_fields
            )
        )

        for fixture_path in fixtures:
            self.loaddata(fixture_path)

    def load_country_self_reference(self, name):
        with self.open_fixture("self/{}".format(name), 'r') as fixture:
            for data in fixture.read():
                country = models.Country.objects.get(cca2=data.object.pk)
                getattr(country, name).add(*data.m2m_data[name])
