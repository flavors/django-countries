import string

import factory
import factory.fuzzy


class FuzzyCode(factory.fuzzy.FuzzyText):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('chars', string.ascii_uppercase)
        super().__init__(*args, **kwargs)


class ContinentFactory(factory.django.DjangoModelFactory):
    code = FuzzyCode(length=2)
    name = factory.fuzzy.FuzzyText(length=16)

    class Meta:
        model = 'countries.Continent'
        django_get_or_create = ('code',)


class CountryFactory(factory.django.DjangoModelFactory):
    cca2 = factory.Faker('country_code')
    continent = factory.SubFactory(ContinentFactory)

    landlocked = True
    calling_codes = []
    alt_spellings = []
    tlds = []

    class Meta:
        model = 'countries.Country'
        django_get_or_create = ('cca2',)


class CurrencyFactory(factory.django.DjangoModelFactory):
    code = factory.Faker('currency_code')
    numeric = FuzzyCode(chars=string.digits, length=3)
    name = factory.fuzzy.FuzzyText(length=16)

    class Meta:
        model = 'countries.Currency'
        django_get_or_create = ('code',)


class DivisionFactory(factory.django.DjangoModelFactory):
    code = factory.fuzzy.FuzzyText(length=8)
    name = factory.fuzzy.FuzzyText(length=16)

    alt_names = []
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = 'countries.Division'
        django_get_or_create = ('country', 'code')


class LanguageFactory(factory.django.DjangoModelFactory):
    cla2 = FuzzyCode(chars=string.ascii_lowercase, length=2)
    cla3 = FuzzyCode(chars=string.ascii_lowercase, length=3)
    name = factory.fuzzy.FuzzyText(length=16)

    class Meta:
        model = 'countries.Language'
        django_get_or_create = ('cla3',)


class LocaleFactory(factory.django.DjangoModelFactory):
    code = factory.Faker('locale')
    country = factory.SubFactory(CountryFactory)
    language = factory.SubFactory(LanguageFactory)

    class Meta:
        model = 'countries.Locale'
        django_get_or_create = ('language', 'country')


class TimezoneFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('timezone')

    class Meta:
        model = 'countries.Timezone'
        django_get_or_create = ('name',)


class CountryNameFactory(factory.django.DjangoModelFactory):
    common = factory.fuzzy.FuzzyText(length=32)

    country = factory.SubFactory(CountryFactory)
    language = factory.SubFactory(LanguageFactory)

    class Meta:
        model = 'countries.CountryName'
        django_get_or_create = ('country', 'language')
