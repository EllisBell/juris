# Generated by Django 2.2.10 on 2020-08-09 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jurisapp', '0009_auto_20200325_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]