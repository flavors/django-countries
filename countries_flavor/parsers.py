from babel.dates import DateTimePattern
from babel.localedata import Alias
from babel.numbers import NumberPattern
from babel.plural import PluralRule


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

"""
locale = Locale.objects.get(code='es_ES')
BabelParser().parse(locale.babel._data.base)

from countries_flavor.parsers import BabelParser

for locale in Locale.objects.all():
    if locale.babel:
        BabelParser().parse(locale.babel._data.base)
"""
