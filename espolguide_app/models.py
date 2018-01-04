from django.contrib.gis.db import models

class Bloques(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=80)
    unidad = models.CharField(max_length=10)
    bloque = models.CharField(max_length=10)
    tipo = models.CharField(max_length=20)
    descripcio = models.CharField(max_length=100)
    area_m2 = models.FloatField()
    geom = models.MultiPolygonField(srid=4236)
    objects = models.GeoManager()


    # Returns the string representation of the model.
    def __str__(self):
        return self.nombre