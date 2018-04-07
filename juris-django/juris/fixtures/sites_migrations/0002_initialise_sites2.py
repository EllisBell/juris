# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-07 10:51
from __future__ import unicode_literals

from django.db import migrations


def set_site_deets(apps, schema_editor):
    """Populate the sites model"""
    """Populate the sites model"""
    Site = apps.get_model('sites', 'Site')
    Site.objects.all().delete()

    # Register SITE_ID = 1
    domain = "jurisprudencia.pt"
    Site.objects.create(id=1, domain=domain, name=domain)


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_site_deets)
    ]
