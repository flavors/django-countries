Setup
=====

Installation
------------

The recommended way to install the Countries Flavor is via pip:

    pip install django-countries-flavor

Add ``'countries_flavor'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        ...
        'countries_flavor'
    ]


Dependencies
------------

``django-countries-flavor`` supports `Django`_ 1.9+ on Python 3.4, 3.5 and 3.6.

.. _Django: http://www.djangoproject.com/


.. warning::

    Postgis database is required


URLconf
-------

Add the django-countries-flavor URLs to your project's URLconf as follows::

    from django.conf.urls import include
    from django.conf.urls import url

    urlpatterns = [
        url(r'^', include('countries_flavor.rest_framework.urls')
    ]


Loaddata
--------

The ``load_countries`` management command loads all fixtures into the database.

    python manage.py load_countries --babel
