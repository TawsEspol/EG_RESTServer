from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db import connection
from .models import *
from django.core.serializers import serialize
#from djgeojson.serializers import Serializer as GeoJSONSerializer

# Create your views here.
def obtenerBloques(request):
	#bloques=serialize('geojson',Bloques.objects.all(),geometry_field='geom',fields=('nombre','tipo','bloque','descripcio','area_m2',))
	#bloques=GeoJSONSerializer().serialize(Bloques.objects.all(), use_natural_keys=True, with_modelname=False)
	
	d={}
	d["type"]="FeatureCollection"
	lista=[]
	bloques=Bloques.objects.all()
	for b in bloques:
		feature_element={}
		feature_element["type"]="Feature"
		feature_element["properties"]={"codigo":b.codigo,"nombre":b.nombre,"unidad":b.unidad,"bloque":b.bloque,"tipo":b.tipo,"descripcio":b.descripcio,"area_m2":b.area_m2}
		geometry={}
		geometry["type"]="Polygon"
		coordenadas_externa=[]
		coordenadas_media=[]
		rango=len(b.geom[0][0])
		for i in range (rango):
			tupla=b.geom[0][0][i]
			coordenadas=[]
			coordenadas.append(tupla[0])
			coordenadas.append(tupla[1])
			coordenadas_media.append(coordenadas)
		coordenadas_externa.append(coordenadas_media)
		geometry["coordinates"]=coordenadas_externa
		lista.append(feature_element)
	d["features"]=lista
	return HttpResponse(json.dumps(d),content_type='application/json')
	#return HttpResponse(json.dumps(bloques),content_type='application/json')