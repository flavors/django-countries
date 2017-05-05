Countries
=========

For example, we could look up the Country:

    >>> country = Country.objects.get(cca2='ID')
    >>> country.timezones.all()
    <QuerySet [<Timezone: Asia/Jakarta>, <Timezone: Asia/Jayapura>, <Timezone: Asia/Makassar>, <Timezone: Asia/Pontianak>]>


Borders
-------

    >>> country.borders.all()
    <QuerySet [<Country: MY>, <Country: PG>, <Country: TL>]>


Geometry Lookups
----------------

Geographic queries with ``Country`` take the following general form:

    >>> qs = Country.objects.filter(mpoly__<lookup_type>=<parameter>)
    >>> qs = Country.objects.exclude(...)


For example:

    >>> from django.contrib.gis.geos import Point
    >>> point = Point(120.0, -5.0)
    >>> Country.objects.filter(mpoly__contains=point)
    <QuerySet [<Country: ID>]>


Distance
--------

    >>> from django.contrib.gis.measure import D
    >>> Country.objects.filter(location__distance_lte=(point, D(km=2000)))
    <QuerySet [<Country: BN>, <Country: CX>, <Country: ID>, <Country: MY>, <Country: SG>, <Country: TL>]>
