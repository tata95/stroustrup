# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_bookcomment_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcomment',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bookcomment',
            name='blocked_reason',
            field=models.CharField(max_length=200, null=True),
        ),
    ]