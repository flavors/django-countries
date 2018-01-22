from django.core.management import call_command

from ... import models
from ...fields import get_one_to_many_fields, get_self_reference_fields
from ._base import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Load data'

    def handle(self, **options):
        self.verbosity = options['verbosity']

        self.load_all()

        for field in get_self_reference_fields(models.Country):
            self.load_country_self_reference(field.name)

    def loaddata(self, fixture_path):
        if not self.is_excluded(fixture_path):
            call_command(
                'loaddata',
                fixture_path.as_posix(),
                verbosity=self.verbosity)

    def get_fixtures(self, **kwargs):
        return sorted((
            fixture for fixture in self._rootdir.glob('**/*.*')
            if 'self' != fixture.parent.stem
        ), **kwargs)

    def load_all(self):
        one_to_many_fields = [
            field.name for field in get_one_to_many_fields(models.Country)
        ]

        # Sorted key: /path/to/fixture.ext < fixture.ext
        fixtures = self.get_fixtures(
            key=lambda path: path.stem if any(
                name in path.stem or path.parent.match(name)
                for name in one_to_many_fields
            ) else path.as_posix())

        for fixture_path in fixtures:
            self.loaddata(fixture_path)

    def load_country_self_reference(self, name):
        with self.open_fixture('self/{}'.format(name), 'r') as fixture:
            for data in fixture.read():
                country = models.Country.objects.get(cca2=data.object.pk)
                getattr(country, name).add(*data.m2m_data[name])
