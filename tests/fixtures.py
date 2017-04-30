import random
import string


from django.contrib.gis import geos
from countries_flavor import models


def get_or_create_country():
    return models.Country.objects.get_or_create(
        cca2=random_code(string.ascii_uppercase, 2),
        defaults={
            'location': geos.Point(0, 1),
            'landlocked': True,
            'alt_spellings': [],
            'calling_codes': [],
            'tlds': []
        })


def random_code(choices, length):
    return ''.join(random.choice(choices) for i in range(length))
