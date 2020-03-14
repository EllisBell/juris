# Generated by Django 2.2.10 on 2020-03-14 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jurisapp', '0002_auto_20200311_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Já existe um utilizador com este email'}, max_length=254, unique=True, verbose_name='Endereço de email'),
        ),
    ]
