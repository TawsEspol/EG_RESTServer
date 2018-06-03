# -*- coding: latin1 -*-
from django.contrib.gis import admin
from .models import *

# Register your models here.

admin.site.register(Bloques)
admin.site.register(Buildings, admin.GeoModelAdmin)
admin.site.register(Unities)




