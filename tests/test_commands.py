from django.core.management import call_command
from django.test import TestCase

from countries import models


class CommandsTests(TestCase):

    def test_command_load_and_dumpcountries(self):
        call_command('loadcountries', verbosity=0)

        self.assertTrue(models.Country.objects.exists())
        self.assertTrue(models.CountryName.objects.exists())
        self.assertTrue(models.Currency.objects.exists())
        self.assertTrue(models.Division.objects.exists())
        self.assertTrue(models.Language.objects.exists())
        self.assertTrue(models.Locale.objects.exists())
        self.assertTrue(models.Timezone.objects.exists())

        call_command('dumpcountries', verbosity=0)
