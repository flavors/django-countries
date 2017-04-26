import random
import string

from django.contrib.gis import geos
from django.test import TestCase

from countries_flavor import models


def random_code(choices, length):
    return ''.join(random.choice(choices) for i in range(length))


class ModelsTests(TestCase):

    def test_models_countries_str(self):
        country_cca2 = random_code(string.ascii_uppercase, 2)
        country = models.Country.objects.create(
            cca2=country_cca2,
            location=geos.Point(0, 1),
            landlocked=True,
            alt_spellings=[],
            calling_codes=[],
            tlds=[])

        self.assertEqual(str(country), country_cca2)

        language_code = random_code(string.ascii_lowercase, 3)
        language = models.Language.objects.create(code=language_code)
        self.assertEqual(str(language), language_code)

        translation = models.Translation.objects.create(
            country=country,
            language=language)

        self.assertTrue(str(translation).startswith(country_cca2))

    def test_models_currency_str(self):
        currency_code = random_code(string.ascii_uppercase, 3)
        currency = models.Currency.objects.create(code=currency_code)
        self.assertEqual(str(currency), currency_code)
