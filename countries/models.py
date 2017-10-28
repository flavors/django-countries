import datetime
import pytz

from django.contrib.contenttypes import fields as generic_fields
from django.contrib.contenttypes.models import ContentType

from django.contrib.gis.db import models
from django.contrib.postgres import fields as pg_fields

from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import fields
from . import managers


class Continent(models.Model):
    code = fields.CodeISOField(
        _('code'),
        length=2,
        primary_key=True,
        regex=r'[A-Z]')

    name = models.CharField(_('name'), max_length=16)

    class Meta:
        ordering = ('code',)
        verbose_name = _('continent')
        verbose_name_plural = _('continents')

    def __str__(self):
        return self.code


class Country(models.Model):
    cca2 = fields.CodeISOField(
        _('code ISO 3166-1 alpha-2'),
        length=2,
        primary_key=True,
        regex=r'[A-Z]')

    cca3 = fields.CodeISOField(
        _('code ISO 3166-1 alpha-3'),
        length=3,
        regex=r'[A-Z]')

    ccn3 = fields.CodeISOField(
        _('code ISO 3166-1 numeric'),
        length=3,
        regex=r'\d')

    cioc = fields.CodeISOField(
        _('code International Olympic Committee'),
        length=3,
        regex=r'[A-Z]')

    continent = models.ForeignKey(
        'Continent',
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('continent'))

    location = models.PointField(null=True)
    mpoly = models.MultiPolygonField(null=True)

    region = models.CharField(_('region'), max_length=64)
    region_code = fields.CodeISOField(
        _('region code'),
        blank=True,
        length=3,
        regex=r'\d')

    subregion = models.CharField(_('subregion'), max_length=64)
    subregion_code = fields.CodeISOField(
        _('subregion code'),
        blank=True,
        length=3,
        regex=r'\d')

    world_region = fields.CodeISOField(
        _('world region code'),
        blank=True,
        length=4,
        regex=r'[A-Z]')

    postal_code = models.NullBooleanField()

    capital = models.CharField(_('capital'), max_length=128)
    independent = models.CharField(
        _('independent'),
        blank=True,
        max_length=64)

    landlocked = models.BooleanField(_('landlocked status'))
    demonym = models.CharField(_('name of residents'), max_length=64)
    area = models.PositiveIntegerField(_('land area in km'), null=True)

    extra = pg_fields.JSONField(null=True)

    calling_codes = pg_fields.ArrayField(
        models.CharField(
            max_length=8,
            validators=[RegexValidator(regex=r'^\d+$')]),
        verbose_name=_('calling codes'))

    international_prefix = models.CharField(
        _('international prefix'),
        blank=True,
        max_length=4)

    national_destination_code_lengths = pg_fields.ArrayField(
        models.PositiveSmallIntegerField(),
        null=True,
        verbose_name=_('national destination code lengths'))

    national_number_lengths = pg_fields.ArrayField(
        models.PositiveSmallIntegerField(),
        null=True,
        verbose_name=_('national number lengths'))

    national_prefix = models.CharField(
        _('national prefix'),
        blank=True,
        max_length=4)

    alt_spellings = pg_fields.ArrayField(
        models.CharField(max_length=128),
        verbose_name=_('alternative spellings'))

    tlds = pg_fields.ArrayField(
        models.CharField(max_length=16),
        verbose_name=_('country code top-level domains'))

    borders = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name=_('land borders'))

    currencies = models.ManyToManyField(
        'Currency',
        verbose_name=_('currencies'))

    languages = models.ManyToManyField(
        'Language',
        verbose_name=_('official languages'))

    timezones = models.ManyToManyField(
        'Timezone',
        verbose_name=_('timezones'))

    translations = generic_fields.GenericRelation('Translation')

    class Meta:
        ordering = ('cca2',)
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.cca2

    @property
    def native_names(self):
        return self.names.filter(language__in=self.languages.all())


class CountryName(models.Model):
    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE,
        verbose_name=_('country'),
        related_name='names')

    language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name=_('language'))

    common = models.CharField(_('common name'), max_length=128)
    official = models.CharField(_('official name'), max_length=128)

    class Meta:
        ordering = ('country', 'language')
        unique_together = ('country', 'language')
        verbose_name = _('country name')
        verbose_name_plural = _('country names')

    def __str__(self):
        return "{self.country} ({self.language}): {self.common}"\
            .format(self=self)


class Currency(models.Model):
    code = fields.CodeISOField(
        _('code ISO 4217'),
        length=3,
        primary_key=True,
        regex=r'[A-Z]')

    numeric = fields.CodeISOField(
        _('code ISO 4217 numeric'),
        blank=True,
        length=3,
        regex=r'\d')

    name = models.CharField(_('name'), max_length=64)
    full_name = models.CharField(_('full name'), blank=True, max_length=64)

    minor_unit = models.PositiveSmallIntegerField(blank=True, null=True)
    symbol = models.CharField(_('symbol'), blank=True, max_length=4)

    unicode_hex = pg_fields.ArrayField(
        models.CharField(max_length=8),
        null=True,
        verbose_name=_('unicode hex'))

    translations = generic_fields.GenericRelation('Translation')

    class Meta:
        ordering = ('code',)
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __str__(self):
        return self.code


class Division(models.Model):
    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE,
        related_name='divisions',
        verbose_name=_('country'))

    code = models.CharField(_('code'), max_length=8, db_index=True)
    name = models.CharField(_('name'), max_length=128)

    alt_names = pg_fields.ArrayField(
        models.CharField(max_length=128),
        verbose_name=_('alternative names'))

    location = models.PointField(null=True)
    poly = models.PolygonField(null=True)

    def __str__(self):
        return "{self.country}: {self.code}".format(self=self)

    class Meta:
        ordering = ('country', 'code')
        unique_together = ('country', 'code')
        verbose_name = _('division')
        verbose_name_plural = _('divisions')


class Language(models.Model):
    name = models.CharField(_('name'), max_length=64)

    cla3 = fields.CodeISOField(
        _('language code ISO 639-3'),
        length=3,
        primary_key=True,
        regex=r'[a-z]')

    cla2 = fields.CodeISOField(
        _('language code ISO 639-1'),
        blank=True,
        length=3,
        regex=r'[a-z]')

    translations = generic_fields.GenericRelation('Translation')

    class Meta:
        ordering = ('cla3',)
        verbose_name = _('language')
        verbose_name_plural = _('languages')

    def __str__(self):
        return self.cla3


class Locale(models.Model):
    code = models.CharField(
        _('code'),
        max_length=16,
        primary_key=True)

    language = models.ForeignKey(
        'Language',
        on_delete=models.PROTECT,
        verbose_name=_('language'),
        related_name='locales')

    country = models.ForeignKey(
        'Country',
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('country'),
        related_name='locales')

    data = pg_fields.JSONField(null=True)

    translations = generic_fields.GenericRelation('Translation')
    objects = managers.LocaleManager()

    class Meta:
        ordering = ('code',)
        verbose_name = _('locale')
        verbose_name_plural = _('locales')

    def __str__(self):
        return self.code

    def __dir__(self):
        return super().__dir__() + list(self.data.keys())

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            if not attr.startswith('_') and\
                    self.data is not None and\
                    attr in self.data:
                return self.data[attr]
            raise

    @property
    def short_code(self):
        if self.country is not None:
            return self.code[:-3]
        return self.code


class Timezone(models.Model):
    name = models.CharField(
        _('name'),
        max_length=128,
        primary_key=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('timezone')
        verbose_name_plural = _('timezones')

    def __str__(self):
        return self.name

    def activate(self):
        timezone.activate(self.pytz)

    def astimezone(self, localtime):
        return localtime.astimezone(self.pytz)

    def localize(self, date_time, **kwargs):
        return self.pytz.localize(date_time, **kwargs)

    def now(self):
        return datetime.datetime.now(self.pytz)

    @property
    def pytz(self):
        return pytz.timezone(self.name)


class Translation(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('content type'))

    object_id = models.CharField(
        db_index=True,
        max_length=64,
        verbose_name=_('content ID'))

    content = generic_fields.GenericForeignKey('content_type', 'object_id')

    locale = models.ForeignKey(
        'Locale',
        on_delete=models.CASCADE,
        related_name='translations',
        verbose_name=_('locale'))

    text = models.CharField(_('text'), max_length=128)

    class Meta:
        ordering = ('content_type', 'object_id', 'locale')
        unique_together = ('content_type', 'object_id', 'locale')
        verbose_name = _('translation')
        verbose_name_plural = _('translations')

    def __str__(self):
        return "{self.content} ({self.locale}): {self.text}"\
            .format(self=self)
