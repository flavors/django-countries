from babel.dates import DateTimePattern
from babel.localedata import Alias
from babel.numbers import NumberPattern
from babel.plural import PluralRule

from .shortcuts import get_babel
from . import models

__all__ = ['load_babel']


class BaseParser(object):

    def default(self, obj):
        raise NotImplementedError('.default(obj) must be implemented')

    def parse(self, obj):
        if isinstance(obj, dict):
            return {key: self.parse(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self.parse(elem) for elem in obj]
        return self.default(obj)


class BabelParser(BaseParser):

    def default(self, obj):
        if isinstance(obj, PluralRule):
            return obj.rules
        elif isinstance(obj, Alias):
            return obj.keys
        elif isinstance(obj, (DateTimePattern, NumberPattern)):
            return obj.__dict__
        return obj


def load_babel(locale, translations=False):
    translation_fields = [
        'currency_names',
        'currency_names_plural',
        'currency_symbols',
        'languages',
        'territories']

    babel_obj = get_babel(locale)

    if babel_obj is not None:
        data = BabelParser().parse(babel_obj._data.base)
        locale.data = {
            key: value for key, value in data.items()
            if key not in translation_fields
        }

        locale.save()

        if translations:
            for code, name in data['territories'].items():
                try:
                    country = models.Country.objects.get(cca2=code)
                except models.Country.DoesNotExist:
                    continue

                translate = models.Translation(
                    content=country,
                    locale=locale,
                    text=name)

                translate.save()
