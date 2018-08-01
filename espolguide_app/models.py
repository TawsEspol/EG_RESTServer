"""Here models"""
import datetime
from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')

class Unities(models.Model):
    """Model for an academic unit in the campus. Goes for faculties, institutes,
     libraries, management units and academic clubs"""
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

# class Blocks(models.Model):
#   """A block is formed by various buildings, and various blocks can
#    make up a unity like a faculty"""
#   code = models.CharField(max_length = 60)
#   name = models.CharField(max_length = 80)
#   unity = models.ForeignKey(Unities, on_delete = models.CASCADE)


class Buildings(models.Model):

    """Model for a building in a campus. A building has salons like offices,
     clasrooms and laboratories"""
    code_infra = models.CharField(max_length=60)
    code_gtsi = models.CharField(max_length=60)
    name = models.CharField(max_length=80)
    name_infra = models.CharField(max_length=80)
    building_type = models.CharField(max_length=60)
    description = models.CharField(max_length=150, null=True, blank=True, verbose_name='type')
    #unity = models.ForeignKey(Unities, to_field = "name", on_delete = models.CASCADE, null = True)
    unity_name = models.CharField(max_length=80, null=True)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.Manager()
    #photo = models.CharField(max_length=250, null=True)
    def __unicode__(self):
        return self.name
          
    def __str__(self):
        return self.name


class Salons(models.Model):
    """Model for a salon inside a building. A salon can be a classroom, laboratory,
     dining room; any room inside a building"""
    name = models.CharField(max_length=80)
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    salon_type = models.CharField(max_length=60)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Users(models.Model):
    """User for app for validate with tokens"""
    REQUIRED_FIELDS = ('user',)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=64, default=None)
    token = models.CharField(max_length=200, default=None)
    USERNAME_FIELD = 'username'
    is_anonymous = False
    is_authenticated = False
    objects = models.Manager()

    # Returns the string representation of the model.
    def __str__(self):
        return self.username

class Favorites(models.Model):
    """Model for save favorites POIs"""
    id_buildings = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    id_users = models.ForeignKey(Users, on_delete=models.CASCADE)
    time_of_create = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

