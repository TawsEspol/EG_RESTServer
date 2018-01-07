from django.core.serializers import serialize
from espolguide_app import *

serialize('geojson',
	Bloques.objects.all(),
	geometry_field='ponit',
	fields=('name',))