from babel.dates import DateTimePattern
from babel.localedata import Alias
from babel.numbers import NumberPattern
from babel.plural import PluralRule

from .shortcuts import get_babel


class BaseParser(object):

    def default(self, obj):
        return obj

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


def load_babel_data(locale):
    translation_fields = [
        'currency_names',
        'currency_names_plural',
        'currency_symbols',
        'languages',
        'territories']

    babel_obj = get_babel(locale)

    if babel_obj is not None:
        locale_data = BabelParser().parse(babel_obj._data.base)
        return {
            key: value for key, value in locale_data.items()
            if key not in translation_fields
        }
