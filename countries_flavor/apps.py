from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CountriesAppConfig(AppConfig):
    name = 'countries_flavor'
    verbose_name = _('Countries')
