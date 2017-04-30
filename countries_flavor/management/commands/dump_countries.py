import os

from django.apps import apps
from django.core.management import call_command

from ...fields import get_many_to_one_fields
from ...fields import get_non_self_reference_fields
from ...fields import get_one_to_many_fields
from ...fields import get_self_reference_fields

from ... import models

from ._base_dumper import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Dump all data'

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

    def dumpdata(self, model_name, path):
        model = "countries_flavor.{model}".format(model=model_name)
        call_command('dumpdata', model, output=path, verbosity=self.verbosity)

    def dump_all(self):
        all_dir = os.path.join(self._rootdir, 'all')

        for fixture in os.listdir(all_dir):
            fixture_path = os.path.join(all_dir, fixture)
            model_name = os.path.splitext(fixture)[0]

            model = apps.get_model(
                app_label=models.__package__,
                model_name=model_name)

            country_field = next((
                field for field in get_many_to_one_fields(model)
                if field.related_model == models.Country), None)

            if country_field is not None:
                with self.open_fixture(fixture_path[:-5], 'w') as fixture:
                    fixture.write(model.objects.filter(**{
                        "{}__isnull".format(country_field.name): True}))
            else:
                self.dumpdata(model_name, fixture_path)

    def get_country_path(self, country, name):
        return "countries/{cca2}.{name}".format(
            cca2=country.cca2.lower(),
            name=name)

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
