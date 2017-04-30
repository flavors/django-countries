Django Countries Flavor
=======================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|

A Django application that provides a list of countries, timezones, currencies, languages, locales and translations.


Dependencies
------------

* Django ≥ 1.9
* PostGIS database (PostgreSQL ≥ 9.4)


Installation
------------

Install last stable version from pypi.

.. code:: sh

    pip install countries-flavor

Add ``countries_flavor`` to your INSTALLED_APPS setting.

.. code:: python

    INSTALLED_APPS = (
        ...
        'countries_flavor.apps.CountriesAppConfig',
    )

Hook the Django Rest Framework urls into your URLconf.

.. code:: python

    from django.conf.urls import include
    from django.conf.urls import url

    urlpatterns = [
        url(r'^', include('countries_flavor.rest_framework.urls')
    ]

Apply migrations.

.. code:: python

    python manage.py migrate


Collect data
------------

The ``load_countries`` management command loads all `fixtures <countries_flavor/fixtures>`__ into the database.

.. code:: sh

    python manage.py load_countries


Standards ISO
-------------

* Country `ISO 3166-1 <https://en.wikipedia.org/wiki/ISO_3166-1>`__
* Currency `ISO 4217 <https://en.wikipedia.org/wiki/ISO_4217>`__
* Language `ISO 639-1 <https://en.wikipedia.org/wiki/ISO_639-1>`__
* Language `ISO 639-3 <https://en.wikipedia.org/wiki/ISO_639-3>`__


Not found!
----------

* Country ISO 3166-1: DG, SH, EA, IC, BQ
* Language ISO 639-1: sh

Credits
-------

* Countries: `mledoze/countries <https://github.com/mledoze/countries>`__
* Locales `Babel <http://babel.pocoo.org>`__
* Languages ISO 639-1 / ISO 639-3: `Wikipedia <https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes>`__
* Currency symbols: `hexorx/currencies <https://github.com/hexorx/currencies>`__
* Divisions and extra data: `rinvex/country <https://github.com/rinvex/country>`__
* Timezones: `antonioribeiro/countries <https://github.com/antonioribeiro/countries>`__
* Country translations `umpirsky/country-list <https://github.com/umpirsky/country-list>`__
* Locale translations `umpirsky/locale-list <https://github.com/umpirsky/locale-list>`__
* Currency translations `umpirsky/currency-list <https://github.com/umpirsky/currency-list>`__


Demo
----

Demo is **NOT** available at `api.domake.io/countries <http://api.domake.io/countries>`__

.. |Pypi| image:: https://img.shields.io/pypi/v/countries-flavor.svg
   :target: https://pypi.python.org/pypi/countries-flavor

.. |Wheel| image:: https://img.shields.io/pypi/wheel/countries-flavor.svg
   :target: https://pypi.python.org/pypi/countries-flavor

.. |Build Status| image:: https://travis-ci.org/flavors/countries.svg?branch=master
   :target: https://travis-ci.org/flavors/countries

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/countries.svg
   :target: https://codecov.io/gh/flavors/countries

.. |Code Climate| image:: https://codeclimate.com/github/flavors/countries/badges/gpa.svg
   :target: https://codeclimate.com/github/flavors/countries
