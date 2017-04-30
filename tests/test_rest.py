from rest_framework.test import APITestCase

from .compat import reverse
from .fixtures import get_or_create_country


class RestFrameworkTests(APITestCase):

    def setUp(self):
        self.country, _ = get_or_create_country()

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
