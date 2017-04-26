import string

from django.contrib.gis import geos
from rest_framework.test import APITestCase

from countries_flavor import models

from .compat import reverse
from .helpers import random_code


class RestFrameworkTests(APITestCase):

    def setUp(self):
        country_cca2 = random_code(string.ascii_uppercase, 2)
        self.country, _ = models.Country.objects.get_or_create(
            cca2=country_cca2,
            defaults={
                'location': geos.Point(0, 1),
                'landlocked': True,
                'alt_spellings': [],
                'calling_codes': [],
                'tlds': []
            })

    def test_country_list_filter(self):
        response = self.client.get(reverse('countries:country-list'), {
            'cca2': self.country.cca2
        })

        features = response.data['features']
        self.assertEqual(len(features), 1)
        self.assertEqual(features[0]['properties']['cca2'], self.country.cca2)

    def test_country_detail(self):
        response = self.client.get(reverse(
            'countries:country-detail', kwargs={
                'pk': self.country.cca2
            }))

        self.assertEqual(
            response.data['properties']['cca2'],
            self.country.cca2)
