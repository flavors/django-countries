from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from countries_flavor import admin
from countries_flavor import models


class MockRequest:
    pass


request = MockRequest()


class AdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_admin_continent(self):
        model_admin = admin.ContinentAdmin(models.Continent, self.site)
        self.assertIn('code', model_admin.get_fields(request))

    def test_admin_country(self):
        model_admin = admin.CountryAdmin(models.Country, self.site)
        self.assertIn('cca2', model_admin.get_fields(request))

    def test_admin_country_name(self):
        model_admin = admin.CountryNameAdmin(models.CountryName, self.site)
        self.assertIn('country', model_admin.get_fields(request))

    def test_admin_currency(self):
        model_admin = admin.CurrencyAdmin(models.Currency, self.site)
        self.assertIn('code', model_admin.get_fields(request))

    def test_admin_division(self):
        model_admin = admin.DivisionAdmin(models.Division, self.site)
        self.assertIn('code', model_admin.get_fields(request))

    def test_admin_language(self):
        model_admin = admin.LanguageAdmin(models.Language, self.site)
        self.assertIn('cla3', model_admin.get_fields(request))

    def test_admin_locale(self):
        model_admin = admin.LocaleAdmin(models.Locale, self.site)
        self.assertIn('code', model_admin.get_fields(request))

    def test_admin_timezone(self):
        model_admin = admin.TimezoneAdmin(models.Timezone, self.site)
        self.assertIn('name', model_admin.get_fields(request))

    def test_admin_translation(self):
        model_admin = admin.TranslationAdmin(models.Translation, self.site)
        self.assertIn('locale', model_admin.get_fields(request))
