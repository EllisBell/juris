# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

# N.B. changing most fields from CharField to TextField (with no max length)
# Hope this doesn't cause issues...
class Acordao(models.Model):
    acordao_id = models.AutoField(primary_key=True)
    processo = models.CharField(max_length=100, blank=True, null=True)
    tribunal = models.ForeignKey('Tribunal', models.DO_NOTHING, blank=True, null=True)
    seccao = models.CharField(max_length=100, blank=True, null=True)
    num_convencional = models.CharField(max_length=100, blank=True, null=True)
    relator = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=50, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    votacao = models.CharField(max_length=50, blank=True, null=True)
    aditamento = models.TextField(blank=True, null=True)
    trib_recorrido = models.TextField(blank=True, null=True)
    proc_trib_recorrido = models.CharField(max_length=100, blank=True, null=True)
    data_dec_recorrida = models.DateField(blank=True, null=True)
    txt_integral_flag = models.CharField(max_length=5, blank=True, null=True)
    txt_parcial_flag = models.CharField(max_length=5, blank=True, null=True)
    privacidade = models.IntegerField(blank=True, null=True)
    meio_processual = models.TextField(blank=True, null=True)
    recorrente = models.TextField(blank=True, null=True)
    decisao = models.TextField(blank=True, null=True)
    indic_eventuais = models.TextField(blank=True, null=True)
    area_tematica = models.TextField(blank=True, null=True)
    doutrina = models.TextField(blank=True, null=True)
    legis_nacional = models.TextField(blank=True, null=True)
    juris_nacional = models.CharField(max_length=-1, blank=True, null=True)
    sumario = models.TextField(max_length=-1, blank=True, null=True)
    txt_parcial = models.TextField(blank=True, null=True)
    txt_integral = models.TextField(blank=True, null=True)
    html_txt_integral = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    date_loaded = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'acordao'


class AcordaoDescritor(models.Model):
    acordao = models.ForeignKey(Acordao, models.DO_NOTHING, blank=True, null=True)
    descritor = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        db_table = 'acordao_descritor'


class AcordaoRecorrido(models.Model):
    acordao = models.ForeignKey(Acordao, models.DO_NOTHING, blank=True, null=True)
    recorrido = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        db_table = 'acordao_recorrido'


class Tribunal(models.Model):
    id_name = models.CharField(primary_key=True, max_length=-1)
    long_name = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        db_table = 'tribunal'
