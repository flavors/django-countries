from django.test import TestCase
from django.apps import apps


class AppConfigTests(TestCase):

    def test_apps_config(self):
        app_config = apps.get_app_config('countries_flavor')
        self.assertEqual(app_config.verbose_name, 'Countries')
