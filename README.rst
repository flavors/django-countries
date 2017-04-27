Countries flavor
================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


Dependencies
------------

* Django >= 1.9
* PostGIS database


Installation
------------

Using pip:

.. code:: sh

    pip install countries-flavor

Add 'countries_flavor' to your INSTALLED_APPS setting.

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


Collect data
------------

The collect_countries management command loads the countries into the database.

.. code:: sh

    python manage.py collect_countries


You can use the option '-c' to specify a comma separated list of countries in ISO 3166-1 alpha-2.

.. code:: sh

    python manage.py collect_countries -c HK,VN
    Installed 2 object(s) from https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json
    Installed 163 object(s) from 1 fixture(s)


Credits
-------

* **Countries**: `mledoze/countries`_
* **Currencies**: `hexorx/currencies`_


Demo
----

Demo is available at `api.domake.io/countries`_


.. _api.domake.io/countries: http://api.domake.io/countries

.. _mledoze/countries: https://github.com/mledoze/countries
.. _hexorx/currencies: https://github.com/hexorx/currencies

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
