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

    def test_admin_country(self):
        model_admin = admin.CountryAdmin(models.Country, self.site)

        self.assertIn('cca2', model_admin.get_fields(request))
        self.assertEqual(
            models.Country.objects.count(),
            model_admin.get_queryset(request).count())

    def test_admin_currency(self):
        model_admin = admin.CurrencyAdmin(models.Currency, self.site)

        self.assertIn('code', model_admin.get_fields(request))
        self.assertEqual(
            models.Currency.objects.count(),
            model_admin.get_queryset(request).count())

    def test_admin_language(self):
        model_admin = admin.LanguageAdmin(models.Language, self.site)

        self.assertIn('code', model_admin.get_fields(request))
        self.assertEqual(
            models.Language.objects.count(),
            model_admin.get_queryset(request).count())

    def test_admin_translation(self):
        model_admin = admin.TranslationAdmin(models.Translation, self.site)

        self.assertIn('language', model_admin.get_fields(request))
        self.assertEqual(
            models.Translation.objects.count(),
            model_admin.get_queryset(request).count())
