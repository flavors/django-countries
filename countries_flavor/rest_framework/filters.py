import rest_framework_filters as filters

from .. import models


class CountryFilter(filters.FilterSet):

    class Meta:
        model = models.Country
        fields = {
            'cca2': ['exact'],
            'cca3': ['exact'],
            'ccn3':  ['exact'],
            'cioc': ['exact'],
            'region': '__all__',
            'subregion': '__all__',
            'capital': '__all__'
        }
