import os

from django.core.management import call_command

from ... import models
from ._base_dumper import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Dump all data'

    def handle(self, **options):
        self.dump_all()
        self.dump_borders()

        # skip borders field serialize
        models.Country._meta.many_to_many = [
            field for field in models.Country._meta.many_to_many
            if field.attname != 'borders'
        ]

        for country in models.Country.objects.all():
            self.dump_country(country)

    @classmethod
    def dumpdata(cls, model_name, path):
        model = "countries_flavor.{model}".format(model=model_name)
        call_command('dumpdata', model, '--output', path)

    def dump_all(self):
        all_dir = os.path.join(self.rootdir, 'all')

        for fixture in os.listdir(all_dir):
            model = os.path.splitext(fixture)[0]
            self.dumpdata(model, os.path.join(all_dir, fixture))

    def dump_borders(self):
        with self.open_fixture('m2m/borders', 'w') as fixture:
            fixture.write(models.Country.objects.all(), fields=('borders',))

    def dump_country(self, country):
        path = "countries/{cca2}.geo".format(cca2=country.cca2.lower())

        with self.open_fixture(path, 'w') as fixture:
            fixture.write([country])

        for related_field in ('divisions', 'names'):
            related_manager = getattr(country, related_field)

            if related_manager.exists():
                related_path = path.replace('geo', related_field)
                with self.open_fixture(related_path, 'w') as fixture:
                    fixture.write(related_manager.all())
