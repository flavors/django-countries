from django.core.management import call_command
from django.test import TestCase


class CommandsTests(TestCase):

    def test_command_countries_setup(self):
        call_command('countries_setup', countries='VN')
