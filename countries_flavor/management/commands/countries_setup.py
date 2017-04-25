import json
import requests

from django.contrib.gis import geos
from django.core.management.base import BaseCommand

from ... import models


class Command(BaseCommand):
    DATASET_URL = 'https://raw.githubusercontent.com/mledoze/countries'

    help = 'Set up :)'

    def handle(self, **options):
        countries = self.request('dist/countries')

        for data in countries:
            area = data['area']
            cca3 = data['cca3']

            geometry = self.request("data/{cca3}.geo".format(
                cca3=cca3.lower())
            )['features'][0].get('geometry')

            if geometry is not None:
                geometry = geos.GEOSGeometry(json.dumps(geometry))

                if isinstance(geometry, geos.Polygon):
                    geometry = geos.MultiPolygon(geometry)

            country, _ = models.Country.objects.update_or_create(
                cca2=data['cca2'],
                defaults={
                    'cca3': cca3,
                    'ccn3': data['ccn3'],
                    'cioc': data['cioc'],
                    'region': data['region'],
                    'subregion': data['subregion'],
                    'capital': data['capital'],
                    'landlocked': data['landlocked'],
                    'demonym': data['demonym'],
                    'area': None if area < 0 else area,
                    'location': geos.Point(data['latlng'][::-1]),
                    'alt_spellings': data['altSpellings'],
                    'calling_codes': data['callingCode'],
                    'tlds': data['tld'],
                    'geo': geometry
                })

            for language_code, name in data['languages'].items():
                language, _ = models.Language.objects.update_or_create(
                    code=language_code,
                    defaults={'name': name})

                country.languages.add(language)

            translations = data['translations']
            translations.update(data['name'].pop('native'))
            translations.update({'eng': data['name']})

            for language_code, name in translations.items():
                language, _ = models.Language.objects\
                    .get_or_create(code=language_code)

                models.CountryName.objects.update_or_create(
                    country=country,
                    language=language,
                    defaults={
                        'common': name['common'],
                        'official': name['official']
                    })

            for currency_code in data['currency']:
                currency, _ = models.Currency.objects\
                    .get_or_create(code=currency_code)

                country.currencies.add(currency)

            self.stdout.write('.', ending='')
            self.stdout.flush()

        for data in countries:
            country = models.Country.objects.get(cca2=data['cca2'])

            for border in data['borders']:
                country.borders.add(models.Country.objects.get(cca3=border))

        self.stdout.write(self.style.SUCCESS('SUCCESS!!'))

    @classmethod
    def request(cls, path):
        return requests.get("{dataset_url}/master/{path}.json".format(
            dataset_url=cls.DATASET_URL,
            path=path
        )).json()
