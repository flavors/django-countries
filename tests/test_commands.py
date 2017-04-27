import mock

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
