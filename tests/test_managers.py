from django.test import TestCase
from countries_flavor import models

from countries_flavor import factories


class ManagersTests(TestCase):

    def test_managers_qs_short_code(self):
        factory = factories.LocaleFactory()
        locale = models.Locale.objects.get(short_code=factory.language.cla2)

        self.assertEqual(factory, locale)

    def test_managers_create_locale(self):
        language = factories.LanguageFactory()
        locale = models.Locale.objects.create_locale(code=language.cla2)

        self.assertIsNone(locale.country)
        self.assertEqual(locale.language, language)
        self.assertEqual(locale.code, language.cla2)

    def test_managers_create_country_locale(self):
        language = factories.LanguageFactory()
        country = factories.CountryFactory()

        locale_code = "{language.cla2}_{country.cca2}".format(
            language=language,
            country=country
        )

        locale = models.Locale.objects.create_locale(code=locale_code)

        self.assertEqual(locale.country, country)
        self.assertEqual(locale.language, language)
        self.assertEqual(locale.code, locale_code)
