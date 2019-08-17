from django.contrib.gis import admin
from .models import *
from leaflet.admin import LeafletGeoAdmin

admin.site.site_header = "ESPOLGuide Admin";
admin.site.title = "ESPOLGuide Admin";

class BuildingsAdmin(LeafletGeoAdmin):
	list_display = ('unity_name','name_espol','code_gtsi',)
	list_filter = ('unity_name',)
	
class NotificationsAdmin(admin.ModelAdmin):
	list_filter = ('event_title',)
	list_display = ('id', 'event_title', 'id_user')

# Register your models here.
admin.site.register(Users)
admin.site.register(Buildings, BuildingsAdmin)
admin.site.register(Unities)
admin.site.register(Salons)
admin.site.register(Favorites)
admin.site.register(Notifications, NotificationsAdmin)



