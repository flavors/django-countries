from django.test import TestCase
from countries_flavor import factories


class ModelsTests(TestCase):

    def test_models_continent_str(self):
        continent = factories.ContinentFactory()
        self.assertEqual(str(continent), continent.code)

    def test_models_countries_str(self):
        country = factories.CountryFactory()
        self.assertEqual(str(country), country.cca2)

    def test_models_language_str(self):
        language = factories.LanguageFactory()
        self.assertEqual(str(language), language.cla3)

    def test_models_country_name_str(self):
        country_name = factories.CountryNameFactory()

        self.assertTrue(
            str(country_name).startswith(country_name.country.cca2)
        )

    def test_models_division_str(self):
        division = factories.DivisionFactory()
        self.assertTrue(str(division).startswith(division.country.cca2))

    def test_models_currency_str(self):
        currency = factories.CurrencyFactory()
        self.assertEqual(str(currency), currency.code)

    def test_models_locale_str(self):
        locale = factories.LocaleFactory()
        self.assertEqual(str(locale), locale.code)

    def test_models_timezone_str(self):
        timezone = factories.TimezoneFactory()
        self.assertEqual(str(timezone), timezone.name)

    def test_models_translation_str(self):
        translation = factories.TranslationFactory()
        # Django 1.9 compatible assert  "None (<locale>): text"
        self.assertTrue(
            str(translation).strip().endswith(str(translation.text))
        )
