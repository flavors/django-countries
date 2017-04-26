from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from . import fields


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

    location = models.PointField()
    geo = models.MultiPolygonField(null=True)

    region = models.CharField(_('region'), max_length=64)
    subregion = models.CharField(_('subregion'), max_length=64)
    capital = models.CharField(_('capital'), max_length=128)
    landlocked = models.BooleanField(_('landlocked status'))
    demonym = models.CharField(_('name of residents'), max_length=64)
    area = models.PositiveIntegerField(_('land area in km'), null=True)

    alt_spellings = ArrayField(
        models.CharField(max_length=128),
        verbose_name=_('alternative spellings'))

    calling_codes = ArrayField(
        models.CharField(
            max_length=8,
            validators=[RegexValidator(regex=r'^\d+$')]),
        verbose_name=_('calling codes'))

    tlds = ArrayField(
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

    class Meta:
        ordering = ('cca2',)
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.cca2


class Translation(models.Model):
    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE,
        verbose_name=_('country'),
        related_name='translations')

    language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name=_('language'))

    common = models.CharField(_('common name'), max_length=128)
    official = models.CharField(_('official name'), max_length=128)

    class Meta:
        ordering = ('country', 'language')
        unique_together = ('country', 'language')

    def __str__(self):
        return "{self.country} ({self.language}): {self.common}"\
            .format(self=self)


class Currency(models.Model):
    code = fields.CodeISOField(
        _('code ISO 4217'),
        length=3,
        primary_key=True,
        regex=r'[A-Z]')

    symbol = models.CharField(_('symbol'), max_length=4)

    class Meta:
        ordering = ('code',)
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.code


class Language(models.Model):
    name = models.CharField(_('name'), max_length=64)
    code = fields.CodeISOField(
        _('language code ISO 639-3'),
        length=3,
        primary_key=True,
        regex=r'[a-z]')

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return self.code
