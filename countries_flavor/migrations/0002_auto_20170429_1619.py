# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 16:19
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries_flavor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
