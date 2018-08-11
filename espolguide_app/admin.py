from django.contrib.gis import admin
from .models import Users, Buildings, Unities, Salons

# Register your models here.

admin.site.register(Users)
admin.site.register(Buildings, admin.GeoModelAdmin)
admin.site.register(Unities)
admin.site.register(Salons)


