from django.contrib.gis.db import models

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
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10)
        
     # Returns the string representation of the model.
    def __str__(self):
        return self.nombre