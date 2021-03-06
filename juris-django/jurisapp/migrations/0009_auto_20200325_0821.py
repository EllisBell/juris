# Generated by Django 2.2.10 on 2020-03-25 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jurisapp', '0008_auto_20200324_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(blank=True)),
            ],
            options={
                'db_table': 'folder',
            },
        ),
        migrations.CreateModel(
            name='SavedAcordao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_at', models.DateTimeField(blank=True)),
                ('acordao', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='jurisapp.Acordao')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='jurisapp.Folder')),
                ('saved_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='jurisapp.User')),
            ],
            options={
                'db_table': 'saved_acordao',
            },
        ),
        migrations.AddField(
            model_name='folder',
            name='acordaos',
            field=models.ManyToManyField(through='jurisapp.SavedAcordao', to='jurisapp.Acordao'),
        ),
        migrations.AddField(
            model_name='folder',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_folders', to='jurisapp.User'),
        ),
        migrations.AddField(
            model_name='folder',
            name='users',
            field=models.ManyToManyField(to='jurisapp.User'),
        ),
        migrations.CreateModel(
            name='AcordaoComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=4000)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='jurisapp.User')),
                ('saved_acordao', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='jurisapp.SavedAcordao')),
            ],
            options={
                'db_table': 'acordao_comment',
            },
        ),
    ]
