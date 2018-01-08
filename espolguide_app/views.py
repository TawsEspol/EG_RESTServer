from django.shortcuts import render

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db import connection
from .models import *
from django.core.serializers import serialize
from pyproj import Proj, transform


# Create your views here.
def obtenerBloques(request):

	d={}
	#d["type"]="FeatureCollection"
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
			#print(tupla[0])
			coordenadas=[]
			coordenadas.append(tupla[0])
			coordenadas.append(tupla[1])
			coordenadas_media.append(coordenadas)
		#print("SE ACABO EL POLIGONO")
		coordenadas_externa.append(coordenadas_media)
		geometry["coordinates"]=coordenadas_externa
		feature_element["geometry"]=geometry
		lista.append(feature_element)
	d["features"]=lista
	d["type"]="FeatureCollection"
	return HttpResponse(json.dumps(d),content_type='application/json')

def transformarCoordenadas(coord1,coord2):
	inProj = Proj(init='epsg:3857')
	outProj = Proj(init='epsg:4326')
	x1,y1 = -11705274.6374,4826473.6922
	x2,y2 = transform(inProj,outProj,x1,y1)
	print x2,y2