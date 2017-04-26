import string

from django.contrib.gis import geos
from django.urls import reverse

from rest_framework.test import APITestCase

from countries_flavor import models
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

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cca2'], self.country.cca2)

    def test_country_detail(self):
        response = self.client.get(reverse(
            'countries:country-detail', kwargs={
                'pk': self.country.cca2
            }))

        self.assertEqual(response.data['cca2'], self.country.cca2)
