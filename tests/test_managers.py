import string

from django.test import TestCase
from countries_flavor import models

from .fixtures import get_or_create_country
from .fixtures import random_code


class ManagersTests(TestCase):

    def test_managers_create_locale(self):
        country, _ = get_or_create_country()

        language_code = random_code(string.ascii_lowercase, 3)
        language = models.Language(cla3=language_code)

        locale_code = "{}_{}".format(language_code, country.cca2)
        locale = models.Locale.objects.create_locale(code=locale_code)

        self.assertEqual(locale.country, country)
        self.assertEqual(locale.language, language)
        self.assertEqual(locale.code, locale_code)
