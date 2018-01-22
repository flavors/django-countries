Setup
=====


Dependencies
------------

``django-countries-flavor`` supports `Django`_ 1.9+ on Python 3.4, 3.5, 3.6 and 3.7.

.. _Django: http://www.djangoproject.com/


.. warning::

    PostGIS database (PostgreSQL ≥ 9.4) is required.


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

The ``loadcountries`` management command read all **fixtures** and re-loaded into the database:

.. code:: sh

    python manage.py loadcountries
