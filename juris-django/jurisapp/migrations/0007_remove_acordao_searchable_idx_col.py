# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-08 07:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jurisapp', '0006_acordao_descritores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acordao',
            name='searchable_idx_col',
        ),
    ]
