"""Here models"""
import datetime
from django.contrib.gis.db import models
from django.conf import settings


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')

class Unities(models.Model):
    """Model for an academic unit in the campus. Goes for faculties, institutes,
     libraries, management units and academic clubs"""
    code = models.CharField(max_length=10, verbose_name="code", default=None)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Zone"

class Buildings(models.Model):
    """Model for a building in a campus. A building has salons like offices,
     clasrooms and laboratories"""
    unity_name = models.CharField(max_length=80, verbose_name="zone") #before it was unity_name
    code_gtsi = models.CharField(max_length=60, verbose_name="code")
    code_infra = models.CharField(max_length=60, verbose_name="code_infrastructure", null=True, blank=True)
    name_espol = models.CharField(max_length=80, verbose_name="name")
    building_type = models.CharField(max_length=60, verbose_name = "type")
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name="description")
    geom = models.MultiPolygonField(srid=4326)
    alternative_names = models.CharField(max_length=500, null=True, blank=True) #alternatives names separated by commas
    objects = models.Manager()
    #photo = models.CharField(max_length=250, null=True)
    def __unicode__(self):
        return self.name_espol
          
    def __str__(self):
        return self.name_espol
    class Meta:
        verbose_name = "Building"


class Salons(models.Model):
    """Model for a salon inside a building. A salon can be a classroom, laboratory,
     dining room; any room inside a building"""
    name_espol = models.CharField(max_length=250, verbose_name="detail")
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    salon_type = models.CharField(max_length=60, null=True, blank=True)
    tag = models.CharField(max_length=60, default=None)
    objects = models.Manager()

    def __str__(self):
        return self.name_espol
    class Meta:
        verbose_name = "Spaces (classrooms,laboratories,offices,...)"


class Users(models.Model):
    """User for app for validate with tokens"""
    REQUIRED_FIELDS = ("user",)
    USERNAME_FIELD = "username"
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
    class Meta:
        verbose_name = "User"

class Favorites(models.Model):
    """Model for save favorites POIs"""
    id_buildings = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    id_users = models.ForeignKey(Users, on_delete=models.CASCADE)
    time_of_create = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    class Meta:
        verbose_name = "Favorite"
