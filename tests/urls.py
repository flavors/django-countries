from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include(
        'countries.rest_framework.urls',
        namespace='countries')),
]
