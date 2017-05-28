from django.contrib.gis import admin

from . import models


@admin.register(models.Continent)
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('=code', '^name')


@admin.register(models.Country)
class CountryAdmin(admin.OSMGeoAdmin):
    list_display = (
        'cca2', 'cca3', 'ccn3', 'cioc', 'continent', 'region', 'subregion',
        'capital', 'landlocked', 'demonym', 'area'
    )

    list_filter = ('continent', 'landlocked')

    search_fields = (
        '=cca2', '=cca3', '=ccn3', '=cioc',
        '^region', '^subregion', '^capital'
    )


@admin.register(models.CountryName)
class CountryNameAdmin(admin.ModelAdmin):
    list_display = ('country',  'language', 'common', 'official')
    list_filter = ('language',)
    search_fields = ('common', 'official')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'code',  'numeric', 'name', 'full_name', 'symbol', 'minor_unit'
    )

    search_fields = ('=code',  '=numeric', '^name', 'full_name', '^symbol')


@admin.register(models.Division)
class DivisionAdmin(admin.OSMGeoAdmin):
    list_display = ('code', 'country', 'name')
    list_filter = ('country',)
    search_fields = ('=code', '^name')


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('cla3',  'cla2', 'name')
    search_fields = ('=cla3', '=cla2', '^name')


@admin.register(models.Locale)
class LocaleAdmin(admin.ModelAdmin):
    list_display = ('code',  'language', 'country')
    search_fields = (
        '=code', '=language__cla2', '=language__cla3', 'country__cca2'
    )


@admin.register(models.Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = list_display


@admin.register(models.Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('content_type',  'object_id', 'locale', 'text')
    list_filter = ('content_type',  'text')
    search_fields = ('locale__code', 'text')
