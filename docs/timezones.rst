Timezones
=========

Retrieve timezones by country:

    >>> country = Country.objects.get(cca2='ID')
    >>> country.timezones.all()
    <QuerySet [<Timezone: Asia/Jakarta>, <Timezone: Asia/Jayapura>, <Timezone: Asia/Makassar>, <Timezone: Asia/Pontianak>]>

    >>> timezone = country.timezones.get(name='Asia/Makassar')


Use the use the ``localize()`` method to localize a naive datetime (datetime with no timezone information): 

    >>> from datetime import datetime
    >>> dtime = datetime(year=2017, month=4, day=2, hour=16, minute=20)
    >>> timezone.localize(dtime)
    datetime.datetime(2017, 4, 2, 16, 20, tzinfo=<DstTzInfo 'Asia/Makassar' WITA+8:00:00 STD>)


`Converting an existing localized time using the standard ``astimezone()``:

    >>> utc_dtime = dtime.replace(tzinfo=pytz.utc)
    >>> timezone.astimezone(utc_dtime)
    datetime.datetime(2017, 4, 3, 0, 20, tzinfo=<DstTzInfo 'Asia/Makassar' WITA+8:00:00 STD>)


Get the current time with ``now()``:

    >>> from datetime import datetime
    >>> timezone = country.timezones.get(name='Asia/Makassar')
    >>> timezone.now()
    datetime.datetime(2017, 5, 2, 16, 15, 13, 626913, tzinfo=<DstTzInfo 'Asia/Makassar' WITA+8:00:00 STD>)


set the current time zone to the end user’s actual time zone with ``activate()``

    >>> timezone.activate()
