'''Script para cargar shapefiles en la base de datos se debe ejecutar en el shell de django'''
from os import listdir
from os.path import isfile, join, abspath, dirname
from django.contrib.gis.utils import LayerMapping
from .models import Buildings, Unities, Salons
from dotenv import read_dotenv
import cv2

#read_dotenv(os.path.join(BASE_DIR, '.env'))
EXCEPTIONS = ["auditorio","biblioteca","administración"]
# Auto-generated `LayerMapping` dictionary for Bloques model
BLOQUES_MAPPING = {
	'code_gtsi': 'code_gtsi',
	'code_infra': 'code_gtsi',
	'name_espol': 'name',
	'unity_name' : 'unity',
	'building_type': 'building_t',
	'description': 'descriptio',
	'geom': 'MULTIPOLYGON',
}
BLOQUES_SHP = abspath(join(dirname(__file__),
										   '../data', 'bloques-integradora.shp'),)
SALONS_FOLDER = abspath(join(dirname(__file__),
										   '../data', 'salons'),)
ZONES_FILE = abspath(join(dirname(__file__),
										   '../data', 'unities.csv'),)

def load_unities():
	"""Function that loads zones from a CSV file into the database"""
	file = open(ZONES_FILE,"r")
	file.readline()
	for line in file:
		data = line.strip().split(",")
		code = data[0]
		name = data[1]
		unidad = Unities(code=code, name = name)
		unidad.save()

	file.close()

def load_buildings(verbose=True):
	"""Fuction that loads buildins objects from a shape file into the database"""
	layer_map = LayerMapping(
		Buildings, BLOQUES_SHP, BLOQUES_MAPPING,
		transform=False, encoding='utf-8',
	)
	layer_map.save(strict=True, verbose=verbose)

def load_salons():
	"""Reads a CSV file and creates and saves salons objects in the
	database. The file format is explained in the documentation."""
	print(SALONS_FOLDER)
	onlyfiles = [f for f in listdir(SALONS_FOLDER) if isfile(join(SALONS_FOLDER, f))]
	for file in onlyfiles:
		print("Cargando salones del archivo "+file)
		file = open(SALONS_FOLDER+"/"+file,"r")
		file.readline()
		for line in file:
			data = line.strip().split(",")
			if(len(data)<10):
				#means the salon has no tag
				continue
			zone_num = data[0]
			building_let = data[2].upper()
			building_code = zone_num+building_let
			tag = building_code+"-"+data[9] #Ex: 9A-U001
			salon_type = data[5].lower()
			if(salon_type=="aula" or salon_type == "oficina"):
				salon_detail = tag
			elif(salon_type.lower() not in EXCEPTIONS):
				salon_detail = data[6].capitalize()
			else:
				salon_detail = data[6]
			#Obtain the building object 
			building = Buildings.objects.filter(code_gtsi=building_code)
			if (len(building) == 1):
				building = building[0] #Get the first element, because filter returns a list
				salon = Salons(name_espol=salon_detail, building=building, salon_type=salon_type, tag=tag)
				salon.save() #save the salon object
			else:
				print("Para el salon "+salon_detail+", la lista de edificion tiene longitud "+str(len(building)))
		file.close()

def run():
	print("Empezando a cargar zonas")
	#load_unities()
	print("Empezando a cargar edificios")
	#load_buildings()
	print("Empezando a cargar salones")
	print("Cargando salones")
	load_salons()
