from django.contrib.gis import admin

from . import models


@admin.register(models.Country)
class CountryAdmin(admin.OSMGeoAdmin):
    list_display = (
        'cca2', 'cca3', 'ccn3', 'cioc', 'region', 'subregion', 'capital',
        'landlocked', 'demonym', 'area')

    list_filter = ('landlocked',)
    search_fields = (
        '=cca2', '=cca3', '=ccn3', '=cioc',
        '^region', '^subregion', '^capital')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code',  'name', 'full_name', 'symbol')
    search_fields = list_display


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code',  'name')
    search_fields = list_display


@admin.register(models.Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('country',  'language', 'common', 'official')
    list_filter = ('language',)
    search_fields = ('common', 'official')
