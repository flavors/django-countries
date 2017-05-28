from babel.dates import DateTimePattern
from babel.localedata import Alias
from babel.numbers import NumberPattern
from babel.plural import PluralRule

from .shortcuts import get_babel
from .shortcuts import get_model


__all__ = ['load_babel', 'load_translations']


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
            load_translations(locale, data)


def load_translations(locale, data):
    Country = get_model('country')

    for code, name in data['territories'].items():
        try:
            country = Country.objects.get(cca2=code)
        except Country.DoesNotExist:
            continue

        translate = get_model('translation')(
            content=country,
            locale=locale,
            text=name
        )

        translate.save()
