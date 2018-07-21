from django.contrib.gis import admin
from .models import *

# Register your models here.

admin.site.register(Users)
admin.site.register(Buildings, admin.GeoModelAdmin)
admin.site.register(Unities)

