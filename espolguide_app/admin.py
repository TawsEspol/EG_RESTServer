# -*- coding: latin1 -*-

from django.contrib.gis import admin
from .models import Bloques,Users, Buildings, Unities

# Register your models here.

admin.site.register(Bloques)
admin.site.register(Users)
admin.site.register(Buildings, admin.GeoModelAdmin)
admin.site.register(Unities)



