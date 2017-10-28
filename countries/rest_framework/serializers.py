from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from .. import models


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Currency
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Language
        fields = '__all__'


class CountryNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CountryName
        exclude = ('id', 'country')


class ListCountrySerializer(gis_serializers.GeoFeatureModelSerializer):
    currencies = CurrencySerializer(many=True)
    languages = LanguageSerializer(many=True)
    translations = CountryNameSerializer(many=True, source='names')

    class Meta:
        model = models.Country
        id_field = False
        exclude = ('mpoly',)
        geo_field = 'location'


class DetailCountrySerializer(ListCountrySerializer):

    class Meta:
        model = models.Country
        id_field = False
        fields = '__all__'
        geo_field = 'mpoly'
