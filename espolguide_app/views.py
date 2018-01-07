from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db import connection
from .models import *
from django.core.serializers import serialize


# Create your views here.
def obtenerBloques(request):
	bloques=serialize('geojson',Bloques.objects.all(),geometry_field='geom',fields=('nombre','tipo','bloque','descripcio','area_m2',))
	return HttpResponse(json.dumps(bloques),content_type='application/json')