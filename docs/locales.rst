Locales
=======

Retrieve locales by country:

    >>> country = Country.objects.get(cca2='ID')
    >>> country.locales.all()
    <LocaleQuerySet [<Locale: id_ID>]>


    >>> locale = country.locales.get(code='id_ID')


Properties
----------

    >>> locale.week_data
    {'first_day': 6, 'min_days': 1, 'weekend_end': 6, 'weekend_start': 5}

    >>> locale.number_symbols
    {'alias': 'None',
     'decimal': ',',
     'exponential': 'E',
     'group': '.',
     'infinity': '∞',
     'list': ';',
     'minusSign': '-',
     'nan': 'NaN',
     'perMille': '‰',
     'percentSign': '%',
     'plusSign': '+',
     'superscriptingExponent': '×',
     'timeSeparator': '.'}

    >>> locale.months['format']['wide']
    {'1': 'Januari',
     '10': 'Oktober',
     '11': 'November',
     '12': 'Desember',
     '2': 'Februari',
     '3': 'Maret',
     '4': 'April',
     '5': 'Mei',
     '6': 'Juni',
     '7': 'Juli',
     '8': 'Agustus',
     '9': 'September'}

    >>> locale.days['format']['wide']
    {'0': 'Senin',
     '1': 'Selasa',
     '2': 'Rabu',
     '3': 'Kamis',
     '4': 'Jumat',
     '5': 'Sabtu',
     '6': 'Minggu'}
