from django.contrib.gis.db import models
from django.conf import settings


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')

class Bloques(models.Model):
    codigo = models.CharField(max_length=60)
    nombre = models.CharField(max_length=80)
    unidad = models.CharField(max_length=60)
    bloque = models.CharField(max_length=60)
    tipo = models.CharField(max_length=60)
    descripcio = models.CharField(max_length=100)
    area_m2 = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.Manager()


    # Returns the string representation of the model.
    def __str__(self):
        return self.nombre

class Users(models.Model):
    """docstring for Users"""
    REQUIRED_FIELDS = ('user',)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=64, default=None)
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = False
    #tender_authority = models.ForeignKey(settings.AUTH_USER_MODEL)
        
     # Returns the string representation of the model.
    def __str__(self):
        return self.username
