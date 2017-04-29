import string
from django.test import TestCase

from countries_flavor import models
from .helpers import random_code


class ModelsTests(TestCase):

    def test_models_continent_str(self):
        continent_code = random_code(string.ascii_uppercase, 3)
        continent = models.Continent(code=continent_code)
        self.assertEqual(str(continent), continent_code)

    def test_models_countries_str(self):
        country_cca2 = random_code(string.ascii_uppercase, 2)
        country = models.Country(cca2=country_cca2)
        self.assertEqual(str(country), country_cca2)

        language_code = random_code(string.ascii_lowercase, 3)
        language = models.Language(cla3=language_code)
        self.assertEqual(str(language), language_code)

        country_name = models.CountryName(
            country=country,
            language=language)

        self.assertTrue(str(country_name).startswith(country_cca2))

        division = models.Division(country=country)
        self.assertTrue(str(division).startswith(country_cca2))

    def test_models_currency_str(self):
        currency_code = random_code(string.ascii_uppercase, 3)
        currency = models.Currency(code=currency_code)
        self.assertEqual(str(currency), currency_code)

    def test_models_locale_str(self):
        locale_code = random_code(string.ascii_letters, 2)
        locale = models.Locale(code=locale_code)
        self.assertEqual(str(locale), locale_code)

    def test_models_timezone_str(self):
        timezone_name = random_code(string.ascii_letters, 16)
        timezone = models.Locale(code=timezone_name)
        self.assertEqual(str(timezone), timezone_name)

    def test_models_translation_str(self):
        locale_code = random_code(string.ascii_letters, 2)
        locale = models.Locale(code=locale_code)

        translation = models.Translation(locale=locale, content=locale)
        self.assertTrue(str(translation).startswith(str(locale)))
