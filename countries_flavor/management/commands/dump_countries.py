import os

from django.core import serializers

from ... import models
from ._base_dumper import DumperBaseCommand


class Command(DumperBaseCommand):
    help = 'Dump all data'

    def handle(self, **options):
        all_path = os.path.join(self.rootdir, 'all')

        for fixture in os.listdir(all_path):
            model = os.path.splitext(fixture)[0]
            self.dumpdata(model, os.path.join(all_path, fixture))

        for country in models.Country.objects.all():
            path = "{path}/countries/{country}.geo.json".format(
                country=country.cca2.lower(),
                path=self.rootdir)

            with open(path, 'w') as fixture:
                fixture.write(serializers.serialize('json', [country]))

            if country.divisions.exists():
                with open(path.replace('geo', 'divisions'), 'w') as fixture:
                    fixture.write(serializers.serialize(
                        'json', country.divisions.all()))
