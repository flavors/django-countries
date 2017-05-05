Setup
=====

Installation
------------

The recommended way to install the Countries Flavor is via pip_::

    pip install countries-flavor

Add ``'countries_flavor'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        ...
        'countries_flavor'
    ]


Dependencies
------------

``countries-flavor`` supports `Django`_ 1.9 through 2.0 on Python 2.7, 3.4, 3.5 and 3.6.

.. _Django: http://www.djangoproject.com/



URLconf
-------

Add the countries-flavor URLs to your project's URLconf as follows::

    from django.conf.urls import include
    from django.conf.urls import url

    urlpatterns = [
        url(r'^', include('countries_flavor.rest_framework.urls')
    ]
