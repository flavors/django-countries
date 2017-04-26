from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    url(r'^', include(
        'countries_flavor.rest_framework.urls',
        namespace='countries')),
]
