import string

from django.test import TestCase
from countries_flavor import models

from .fixtures import get_or_create_country
from .fixtures import random_code


class ManagersTests(TestCase):

    def test_managers_create_locale(self):
        country, _ = get_or_create_country()

        language = models.Language.objects.create(
            cla2=random_code(string.ascii_lowercase, 2)
        )

        locale_code = "{}_{}".format(language.cla2, country.cca2)
        locale = models.Locale.objects.create_locale(code=locale_code)

        self.assertEqual(locale.country, country)
        self.assertEqual(locale.language, language)
        self.assertEqual(locale.code, locale_code)
