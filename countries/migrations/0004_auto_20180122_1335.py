# Generated by Django 2.0.1 on 2018-01-22 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0003_auto_20170529_2300'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='translation',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='translation',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='translation',
            name='locale',
        ),
        migrations.DeleteModel(
            name='Translation',
        ),
    ]
