Django Countries Flavor
=======================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|

A Django application that provides a **data collection** for **internationalization** and **localization** purposes.

Full **documentation** for the project is available at `docs`_.

.. _docs: http://django-countries-flavor.readthedocs.io/en/latest/?badge=latest


Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11
* PostGIS database (PostgreSQL ≥ 9.4)


Installation
------------

Install last stable version from pypi.

.. code:: sh

    pip install django-countries-flavor


Add ``countries`` to your *INSTALLED_APPS* settings:

.. code:: python

    INSTALLED_APPS = [
        ...
        'countries.apps.CountriesAppConfig',
    ]


Apply **migrations**:

.. code:: python

    python manage.py migrate


Load data
---------

The ``loadcountries`` management command read all `fixtures <countries/fixtures>`__ and re-loaded into the database:

.. code:: sh

    python manage.py loadcountries


Standards ISO
-------------

* Country `ISO 3166-1 <https://en.wikipedia.org/wiki/ISO_3166-1>`__
* Currency `ISO 4217 <https://en.wikipedia.org/wiki/ISO_4217>`__
* Language `ISO 639-1 <https://en.wikipedia.org/wiki/ISO_639-1>`__
* Language `ISO 639-3 <https://en.wikipedia.org/wiki/ISO_639-3>`__


Credits
-------

* Countries: `mledoze/countries <https://github.com/mledoze/countries>`__
* Locales `Babel <http://babel.pocoo.org>`__
* Languages ISO 639-1 / ISO 639-3: `Wikipedia <https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes>`__
* Currency symbols: `hexorx/currencies <https://github.com/hexorx/currencies>`__
* Divisions and extra data: `rinvex/country <https://github.com/rinvex/country>`__
* Timezones: `antonioribeiro/countries <https://github.com/antonioribeiro/countries>`__

.. |Pypi| image:: https://img.shields.io/pypi/v/django-countries-flavor.svg
   :target: https://pypi.python.org/pypi/django-countries-flavor

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-countries-flavor.svg
   :target: https://pypi.python.org/pypi/django-countries-flavor

.. |Build Status| image:: https://travis-ci.org/flavors/django-countries.svg?branch=master
   :target: https://travis-ci.org/flavors/django-countries

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-countries.svg
   :target: https://codecov.io/gh/flavors/django-countries

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/1d36caa7d66dd4af9c06/maintainability
   :target: https://codeclimate.com/github/flavors/django-countries
