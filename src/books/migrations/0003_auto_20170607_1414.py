# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20170607_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
