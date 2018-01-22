import re

from django.db import models

from .shortcuts import get_model

__all__ = ['LocaleManager']


locale_regex = re.compile(r'.*_([A-Z]{2})$')


class BaseLocaleManager(models.Manager):

    def create_locale(self, code):
        language = get_model('language').objects.get(cla2=code[:2])
        country_match = locale_regex.match(code)

        if country_match is not None:
            country = get_model('country').objects\
                .get(cca2=country_match.group(1))
        else:
            country = None

        return self.create(code=code, language=language, country=country)


class LocaleQuerySet(models.QuerySet):

    def get(self, **kwargs):
        if 'short_code' in kwargs:
            kwargs['language__cla2'] = kwargs.pop('short_code')
        return super().get(**kwargs)


LocaleManager = BaseLocaleManager.from_queryset(LocaleQuerySet)
