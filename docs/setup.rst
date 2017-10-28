Setup
=====

Installation
------------

The recommended way to install the Countries Flavor is via pip:

    pip install django-countries-flavor

Add ``'countries'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        ...
        'countries'
    ]


Dependencies
------------

``django-countries-flavor`` supports `Django`_ 1.9+ on Python 3.4, 3.5 and 3.6.

.. _Django: http://www.djangoproject.com/


.. warning::

    Postgis database is required


Loaddata
--------

The ``loadcountries`` management command loads all fixtures into the database.

    python manage.py loadcountries
