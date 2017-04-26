from rest_framework_gis import serializers
from .. import models


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Currency
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Language
        fields = '__all__'


class TranslationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Translation
        exclude = ('id', 'country')


class ListCountrySerializer(serializers.GeoFeatureModelSerializer):
    currencies = CurrencySerializer(many=True)
    languages = LanguageSerializer(many=True)
    translations = TranslationSerializer(many=True)

    class Meta:
        model = models.Country
        exclude = ('geo',)
        geo_field = 'location'


class DetailCountrySerializer(ListCountrySerializer):

    class Meta:
        model = models.Country
        fields = '__all__'
        geo_field = 'geo'
