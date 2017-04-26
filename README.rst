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


Demo
----

Demo is available at `api.domake.io`_

.. _domake.io: https://domake.io
.. _api.domake.io: http://api.domake.io/countries

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
