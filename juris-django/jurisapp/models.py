from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Max
from datetime import datetime, timedelta


class Tribunal(models.Model):
    id_name = models.CharField(primary_key=True, max_length=6)
    long_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tribunal'


class AcordaoManager(models.Manager):
    def recent(self):
        most_recent_date = Acordao.objects.aggregate(Max('date_loaded'))['date_loaded__max']
        recent_date = most_recent_date - timedelta(days=3)
        return super().get_queryset().filter(date_loaded__gte=recent_date).order_by('-data')


class Acordao(models.Model):
    acordao_id = models.AutoField(primary_key=True)
    processo = models.TextField(blank=True, null=True)
    tribunal = models.ForeignKey('Tribunal', models.DO_NOTHING, blank=True, null=True)
    seccao = models.TextField(blank=True, null=True)
    num_convencional = models.TextField(blank=True, null=True)
    relator = models.TextField(blank=True, null=True)
    numero = models.TextField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    votacao = models.TextField(blank=True, null=True)
    aditamento = models.TextField(blank=True, null=True)
    trib_recorrido = models.TextField(blank=True, null=True)
    proc_trib_recorrido = models.TextField(blank=True, null=True)
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
    juris_nacional = models.TextField(blank=True, null=True)
    sumario = models.TextField(max_length=-1, blank=True, null=True)
    txt_parcial = models.TextField(blank=True, null=True)
    txt_integral = models.TextField(blank=True, null=True)
    html_txt_parcial = models.TextField(blank=True, null=True)
    html_txt_integral = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    date_loaded = models.DateTimeField(blank=True, null=True)
    descritores = models.TextField(blank=True, null=True)

    objects = AcordaoManager()

    def __str__(self):
        return self.processo

    def get_absolute_url(self):
        return reverse('acordao', kwargs={'acordao_id': self.acordao_id})

    # This is here because the the descritores are saved in the DB as one string
    # (for more efficient storing and retrieving of them)
    # But need to be split up for displaying, indexing in elasticsearch etc.
    def descritores_as_list(self):
        if self.descritores is None:
            return []
        return self.descritores.split("|")

    def set_descritores_to_list(self):
        desc_list = self.descritores_as_list()
        self.descritores = desc_list

    class Meta:
        db_table = 'acordao'


class AcordaoRecorrido(models.Model):
    acordao_recorrido_id = models.AutoField(primary_key=True)
    acordao = models.ForeignKey(Acordao, models.DO_NOTHING, blank=True, null=True)
    recorrido = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'acordao_recorrido'


class SearchHistory(models.Model):
    term = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'search_history'

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('Endereço de email'), unique=True, 
                                error_messages={'unique': 'Já existe um utilizador com este email'})

    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'auth_user'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.TextField(max_length=100, blank=True, null=True)


    class Meta:
        db_table = 'customer'

# Explicitly defining many-to-many table here
# As compared to e.g. the users ManyToManyField on Folder
class CustomerUser(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'customer_user'

    def __str__(self):
        return "{0} in customer {1}".format(self.user.email, self.customer.customer_id)


class Folder(models.Model):
    name = models.TextField(max_length=200)
    description = models.TextField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='created_folders')
    acordaos = models.ManyToManyField(Acordao, through='SavedAcordao')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    archived = models.BooleanField(default=False)

    class Meta:
        db_table = 'folder'

    def __str__(self):
        return self.name

# n.b. many to many table used as 'through' on folder.acordaos above
class SavedAcordao(models.Model):
    acordao = models.ForeignKey(Acordao, models.DO_NOTHING)
    folder = models.ForeignKey(Folder, models.DO_NOTHING)
    saved_at = models.DateTimeField(blank=True)
    saved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'saved_acordao'

    def __str__(self):
        return "{0} in {1}".format(self.acordao.processo, self.folder.name)


class AcordaoComment(models.Model):
    saved_acordao = models.ForeignKey(SavedAcordao, models.DO_NOTHING)
    text = models.TextField(max_length=4000)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'acordao_comment'
