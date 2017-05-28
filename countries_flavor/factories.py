import string

import factory
import factory.fuzzy

from django.contrib.contenttypes.models import ContentType


class ContinentFactory(factory.django.DjangoModelFactory):
    code = factory.fuzzy.FuzzyText(chars=string.ascii_uppercase, length=2)
    name = factory.fuzzy.FuzzyText(length=16)

    class Meta:
        model = 'countries_flavor.Continent'
        django_get_or_create = ('code',)


class CountryFactory(factory.django.DjangoModelFactory):
    cca2 = factory.fuzzy.FuzzyText(chars=string.ascii_uppercase, length=2)
    cca3 = factory.fuzzy.FuzzyText(chars=string.ascii_uppercase, length=3)
    ccn3 = factory.fuzzy.FuzzyText(chars=string.digits, length=3)
    cioc = factory.fuzzy.FuzzyText(chars=string.ascii_uppercase, length=3)

    continent = factory.SubFactory(ContinentFactory)

    landlocked = True
    calling_codes = list()
    alt_spellings = list()
    tlds = list()

    class Meta:
        model = 'countries_flavor.Country'
        django_get_or_create = ('cca2',)


class CurrencyFactory(factory.django.DjangoModelFactory):
    code = factory.fuzzy.FuzzyText(chars=string.ascii_uppercase, length=3)
    numeric = factory.fuzzy.FuzzyText(chars=string.digits, length=3)
    name = factory.fuzzy.FuzzyText(length=16)

    class Meta:
        model = 'countries_flavor.Currency'
        django_get_or_create = ('code',)


class DivisionFactory(factory.django.DjangoModelFactory):
    code = factory.fuzzy.FuzzyText(length=8)
    name = factory.fuzzy.FuzzyText(length=16)

    alt_names = list()
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = 'countries_flavor.Division'
        django_get_or_create = ('country', 'code')


class LanguageFactory(factory.django.DjangoModelFactory):
    cla3 = factory.fuzzy.FuzzyText(chars=string.ascii_lowercase, length=3)
    cla2 = factory.fuzzy.FuzzyText(chars=string.ascii_lowercase, length=2)
    name = factory.fuzzy.FuzzyText(length=16)

    class Meta:
        model = 'countries_flavor.Language'
        django_get_or_create = ('cla3',)


class LocaleFactory(factory.django.DjangoModelFactory):
    code = factory.fuzzy.FuzzyText(length=16)

    language = factory.SubFactory(LanguageFactory)
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = 'countries_flavor.Locale'
        django_get_or_create = ('language', 'country')


class TimezoneFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText(length=32)

    class Meta:
        model = 'countries_flavor.Timezone'
        django_get_or_create = ('name',)


class CountryNameFactory(factory.django.DjangoModelFactory):
    common = factory.fuzzy.FuzzyText(length=32)

    country = factory.SubFactory(CountryFactory)
    language = factory.SubFactory(LanguageFactory)

    class Meta:
        model = 'countries_flavor.CountryName'
        django_get_or_create = ('country', 'language')


class TranslationFactory(factory.django.DjangoModelFactory):
    text = factory.fuzzy.FuzzyText(length=32)
    locale = factory.SubFactory(LocaleFactory)

    content_type = factory.LazyAttribute(
        lambda obj: ContentType.objects.get_for_model(obj.content)
    )

    object_id = factory.SelfAttribute('content.cca2')
    content = factory.SubFactory(CountryFactory)

    class Meta:
        model = 'countries_flavor.Translation'
        exclude = ('content',)
        django_get_or_create = ('locale', 'content_type', 'object_id')
