# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_readerslistrecord_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcomment',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='books.Book'),
            preserve_default=False,
        ),
    ]
