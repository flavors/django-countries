from django.test import TestCase

from countries_flavor.models import Country


class ModelsTests(TestCase):

    def test_models_country(self):
        Country.objects.create(cca2='HK')
