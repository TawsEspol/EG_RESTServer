from django.contrib.gis.db import models
from django.conf import settings


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')

class Unities(models.Model):
	"""Model for an academic unit in the campus. Goes for faculties, institutes, libraries, management units and academic clubs"""
	name = models.CharField(max_length = 150, unique = True)
	description = models.CharField(max_length = 250, null = True, blank = True)
	

	def __str__(self):
		return self.name

# class Blocks(models.Model):
# 	"""A block is formed by various buildings, and various blocks can make up a unity like a faculty"""
# 	code = models.CharField(max_length = 60)
# 	name = models.CharField(max_length = 80)
# 	unity = models.ForeignKey(Unities, on_delete = models.CASCADE)


class Buildings(models.Model):
	"""Model for a building in a campus. A building has salons like offices, clasrooms and laboratories"""
	code_infra = models.CharField(max_length = 60)
	code_gtsi = models.CharField(max_length = 60)
	name = models.CharField(max_length = 80)
	name_infra = models.CharField(max_length = 80)
	building_type = models.CharField(max_length = 60)
	description = models.CharField(max_length = 150, null = True, blank = True)
	unity = models.ForeignKey(Unities, to_field = "name", on_delete = models.CASCADE, null = True)
	geom = models.MultiPolygonField(srid = 4326)
	objects = models.Manager()
	

class Salons(models.Model):
	"""Model for a salon inside a building. A salon can be a classroom, laboratory, dining room; any room inside a building"""
	name = models.CharField(max_length = 80)
	building = models.ForeignKey(Buildings, on_delete = models.CASCADE)
	salon_type = models.CharField(max_length = 60)

	def __str__(self):
		return self.name


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
    token = models.CharField(max_length=200, default=None)
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = False
    #tender_authority = models.ForeignKey(settings.AUTH_USER_MODEL)
        
    # Returns the string representation of the model.
    def __str__(self):
        return self.username
