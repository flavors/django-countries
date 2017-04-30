import re

from django.db import models

from .loaddata import load_babel_data
from .shortcuts import get_model


class LocaleManager(models.Manager):

    def create_locale(self, code, regex=re.compile(r'.*_([A-Z]{2})$')):
        language = get_model('language').objects.get(cla2=code[:2])
        country_match = regex.match(code)

        if country_match is not None:
            country = get_model('country').objects\
                .get(cca2=country_match.group(1))
        else:
            country = None

        return self.create(code=code, language=language, country=country)

    def load_babel_data(self):
        for locale in self.all():
            locale.data = load_babel_data(locale)
            locale.save()
