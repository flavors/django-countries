import json
import requests

from django.contrib.gis import geos
from django.core.management.base import BaseCommand

from ... import models


class Command(BaseCommand):
    DATASET_URL = 'https://raw.githubusercontent.com/mledoze/countries'

    help = 'Set up :)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--countries', '-c',
            dest='countries',
            help='Comma separated country list ISO 3166-1 alpha-2')

    def handle(self, **options):
        countries = self.request('dist/countries')
        country_codes = options['countries'].split(',')

        if country_codes:
            countries = [
                country for country in countries
                if country['cca2'] in country_codes]

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

            self.add_currencies(country, data['currency'])
            self.add_languages(country, data['languages'])

            translations = data['translations']
            translations.update(data['name'].pop('native'))
            translations.update({'eng': data['name']})

            self.add_translations(country, translations)

            self.stdout.write('.', ending='')
            self.stdout.flush()

        self.add_borders(countries)
        self.stdout.write(self.style.SUCCESS(' SUCCESS!!'))

    @classmethod
    def request(cls, path):
        return requests.get("{dataset_url}/master/{path}.json".format(
            dataset_url=cls.DATASET_URL,
            path=path
        )).json()

    @classmethod
    def add_borders(cls, countries):
        for data in countries:
            country = models.Country.objects.get(cca2=data['cca2'])

            for border in data['borders']:
                country.borders.add(models.Country.objects.get(cca3=border))

    @classmethod
    def add_currencies(cls, country, currencies):
        for currency_code in currencies:
            currency, _ = models.Currency.objects\
                .get_or_create(code=currency_code)

            country.currencies.add(currency)

    @classmethod
    def add_languages(cls, country, languages):
        for language_code, name in languages.items():
            language, _ = models.Language.objects.update_or_create(
                code=language_code,
                defaults={'name': name})

            country.languages.add(language)

    @classmethod
    def add_translations(cls, country, translations):
        for language_code, name in translations.items():
            language, _ = models.Language.objects\
                .get_or_create(code=language_code)

            models.Translation.objects.update_or_create(
                country=country,
                language=language,
                defaults={
                    'common': name['common'],
                    'official': name['official']
                })
