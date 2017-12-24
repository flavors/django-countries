from django.apps import apps
from django.test import TestCase


class AppConfigTests(TestCase):

    def test_apps_config(self):
        app_config = apps.get_app_config('countries')
        self.assertEqual(app_config.verbose_name, 'Countries')
