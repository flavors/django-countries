from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from countries_flavor import models


class CommandsTests(TestCase):

    @mock.patch('countries_flavor.management.commands.collect_countries'
                '.Command.request', new=lambda cls, path: [])
    def test_command_collect_countries(self):
        call_command('collect_countries')

    def test_command_collected_countries_list(self):
        countries = ('AD', 'FR', 'XK')
        call_command('collect_countries', countries=','.join(countries))

        manager = models.Country.objects

        self.assertEqual(
            manager.filter(cca2__in=countries).count(),
            len(countries))

        border = manager.get(cca2='AD').borders.get(cca2='FR')
        self.assertTrue(border.cca2, 'FR')

    def test_command_load_and_dump_countries(self):
        call_command('load_countries', babel=True, verbosity=0)

        self.assertTrue(models.Country.objects.exists())
        self.assertTrue(models.CountryName.objects.exists())
        self.assertTrue(models.Currency.objects.exists())
        self.assertTrue(models.Division.objects.exists())
        self.assertTrue(models.Language.objects.exists())
        self.assertTrue(models.Locale.objects.exists())
        self.assertTrue(models.Timezone.objects.exists())
        # self.assertTrue(models.Translation.objects.exists())

        call_command('dump_countries', verbosity=0)
