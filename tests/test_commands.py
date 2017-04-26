from django.core.management import call_command
from django.test import TestCase

from countries_flavor import models


class CommandsTests(TestCase):

    def test_command_countries_setup(self):
        countries = ('AD', 'FR')
        call_command('countries_setup', countries=','.join(countries))

        manager = models.Country.objects
        self.assertEqual(manager.filter(cca2__in=countries).count(), 2)

        border = manager.get(cca2=countries[0]).borders.get(cca2=countries[1])
        self.assertTrue(border.cca2, countries[1])

        border = manager.get(cca2=countries[1]).borders.get(cca2=countries[0])
        self.assertTrue(border.cca2, countries[0])
