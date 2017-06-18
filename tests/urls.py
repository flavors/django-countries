from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include(
        'countries_flavor.rest_framework.urls',
        namespace='countries')),
]
