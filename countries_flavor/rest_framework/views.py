from rest_framework import permissions
from rest_framework import viewsets

from .. import models
from . import filters
from . import serializers


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Country.objects\
        .prefetch_related(
            'borders',
            'currencies',
            'languages',
            'timezones',
            'translations')

    permission_classes = (permissions.AllowAny,)
    filter_class = filters.CountryFilter
    search_fields = (
        '=cca2', '=cca3', '=ccn3', '=cioc',
        '^region', '^subregion', '^capital')

    ordering_fields = ('=cca2', '=cca3', '=ccn3', '=cioc')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ListCountrySerializer
        return serializers.DetailCountrySerializer
