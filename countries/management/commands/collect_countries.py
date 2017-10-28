import json
import requests

from django.contrib.gis import geos
from django.core.management.base import BaseCommand

from ... import models


class Command(BaseCommand):
    DATASET_URL = 'https://raw.githubusercontent.com/mledoze/countries'

    help = 'Collect countries dataset :)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--countries', '-c',
            dest='countries',
            help='Comma separated list of countries in ISO 3166-1 alpha-2'
        )

    def handle(self, **options):
        countries_path = 'dist/countries'
        countries = self.request(countries_path)
        country_codes = options['countries']

        if country_codes is not None:
            countries = [
                country for country in countries
                if country['cca2'] in country_codes.split(',')
            ]

        for data in countries:
            country, _ = self.update_or_create_country(data)

            self.add_currencies(country, data['currency'])
            self.add_languages(country, data['languages'])

            translations = data['translations']
            translations.update(data['name'].pop('native'))
            translations.update({'eng': data['name']})

            self.add_translations(country, translations)

            self.stdout.write('.', ending='')
            self.stdout.flush()

        self.add_borders(countries)

        self.stdout.write(
            "\nInstalled {count} object(s) from {url}".format(
                count=len(countries),
                url=self.endpoint(countries_path)
            ))

    @classmethod
    def endpoint(cls, path):
        return "{dataset_url}/master/{path}.json".format(
            dataset_url=cls.DATASET_URL,
            path=path
        )

    @classmethod
    def request(cls, path):
        return requests.get(cls.endpoint(path)).json()

    @classmethod
    def update_or_create_country(cls, data):
        area = data['area']
        cca3 = data['cca3']

        geometry = cls.request("data/{cca3}.geo".format(
            cca3=cca3.lower())
        )['features'][0].get('geometry')

        if geometry is not None:
            geometry = geos.GEOSGeometry(json.dumps(geometry))

            if isinstance(geometry, geos.Polygon):
                geometry = geos.MultiPolygon(geometry)

        return models.Country.objects.update_or_create(
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
                'mpoly': geometry
            }
        )

    @classmethod
    def add_borders(cls, countries):
        for data in countries:
            country = models.Country.objects.get(cca2=data['cca2'])

            for cca3 in data['borders']:
                try:
                    country_border = models.Country.objects.get(cca3=cca3)
                except models.Country.DoesNotExist:
                    continue
                country.borders.add(country_border)

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
                cla3=language_code,
                defaults={'name': name}
            )

            country.languages.add(language)

    @classmethod
    def add_translations(cls, country, translations):
        for language_code, name in translations.items():
            language, _ = models.Language.objects\
                .get_or_create(cla3=language_code)

            models.CountryName.objects.update_or_create(
                country=country,
                language=language,
                defaults={
                    'common': name['common'],
                    'official': name['official']
                }
            )
