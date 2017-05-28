from django.core.management import call_command

from ...fields import get_first_related_model_field
from ...fields import get_non_self_reference_fields
from ...fields import get_one_to_many_fields
from ...fields import get_self_reference_fields

from ... import models
from ...shortcuts import get_model

from ._base import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Dump data'

    exclude_fixtures = (
        'all/locale*',
        'countries/*.locales*'
    )

    def handle(self, **options):
        self.verbosity = options['verbosity']

        self.dump_all()
        self_reference_fields = get_self_reference_fields(models.Country)

        for field in self_reference_fields:
            self.dump_country_self_reference(field.name)

        # skip self reference field serialize
        models.Country._meta.many_to_many =\
            get_non_self_reference_fields(models.Country)

        for country in models.Country.objects.all():
            self.dump_country(country)

    def dumpdata(self, model_name, fixture_path):
        if not self.is_excluded(fixture_path):
            model_name = "countries_flavor.{model}".format(model=model_name)

            call_command(
                'dumpdata',
                model_name,
                output=fixture_path.as_posix(),
                verbosity=self.verbosity
            )

    def dump_all(self):
        for fixture_path in (self._rootdir / 'all').iterdir():
            model = get_model(model_name=fixture_path.stem)

            country_field =\
                get_first_related_model_field(model, models.Country)

            if country_field is not None:
                with self.open_fixture(fixture_path, 'w') as fixture:
                    fixture.write(
                        model.objects.filter(**{
                            "{}__isnull".format(country_field.name): True
                        })
                    )
            else:
                self.dumpdata(fixture_path.stem, fixture_path)

    def dump_country_self_reference(self, name):
        with self.open_fixture("self/{}".format(name), 'w') as fixture:
            fixture.write(models.Country.objects.all(), fields=(name,))

    def dump_country_one_to_many(self, country, name):
        manager = getattr(country, name)
        path = self.get_country_path(country, name)

        if manager.exists():
            with self.open_fixture(path, 'w') as fixture:
                fixture.write(manager.all())

    def dump_country(self, country):
        path = self.get_country_path(country, 'geo')

        with self.open_fixture(path, 'w') as fixture:
            fixture.write([country])

        for related_name in get_one_to_many_fields(models.Country):
            self.dump_country_one_to_many(country, related_name.name)
