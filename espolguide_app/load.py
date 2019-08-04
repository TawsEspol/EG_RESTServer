'''Script para cargar shapefiles en la base de datos se debe ejecutar en el shell de django'''
import os
from django.contrib.gis.utils import LayerMapping
from .models import Buildings, Unities, Salons
from dotenv import read_dotenv
import cv2

#read_dotenv(os.path.join(BASE_DIR, '.env'))

# Auto-generated `LayerMapping` dictionary for Bloques model
BLOQUES_MAPPING = {
    'code_infra': 'code_infra',
    'code_gtsi': 'code_gtsi',
    'name_espol': 'name_espol',
    'unity_name' : 'unity',
    'building_type': 'building_t',
    'description': 'descriptio',
    'geom': 'MULTIPOLYGON',
}
BLOQUES_SHP = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           '../data', 'bloques-unificados-con-geometria.shp'),)
DEFAULT_SALONS_FILE = "/home/belen/github/EG_RESTServer/data/aULAS_2018_espolguide.csv"
DEFAULT_UNITIES__FILE = "dumps/unidades.txt"

#BLOQUES_SHP = os.getenv('SHAPES_PATH')
def load_buildings(verbose=True):
    '''Funcion para cargar los shapefiles'''
    layer_map = LayerMapping(
        Buildings, BLOQUES_SHP, BLOQUES_MAPPING,
        transform=False, encoding='utf-8',
    )
    layer_map.save(strict=True, verbose=verbose)

def load_unities(_file_path=DEFAULT_UNITIES__FILE):
    file = open(_file_path,"r")
    for line in file:
        data = line.strip().split("\t")
        name = data[0]
        unidad = Unities(name = name)
        if len(data)==2:
            description = data[1]
            unidad.description = description
        unidad.save()

    file.close()

def load_salons(_file_path=DEFAULT_SALONS_FILE):
	"""Receives a CSV file and saves Salon instances per each row in the database.
	"""
    file = open(_file_path,"r")
    file.readline()
    for line in file:
        data = line.strip().split(",")
        salon_name = data[2]
        building_code = data[3]
        building = Buildings.objects.filter(code_gtsi=building_code)
        if (len(building) == 1):
            building = building[0]
            salon = Salons(name_espol=salon_name, building=building)
            salon.save()
        else:
            print(building_code)
    file.close()

def compress_statics():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(BASE_DIR,"img")
    img_dirs = [os.path.join(static_dir, f) for f in os.listdir(static_dir)]
    for img_dir in img_dirs:
        img = os.listdir(img_dir)[0]
        img_path = img_dir+"/"+img
        if (img!="espol.png"):
            photo = cv2.imread(img_path)
            resized = cv2.resize(photo, (640,480), interpolation = cv2.INTER_AREA)
            cv2.imwrite(img_path, resized)

if __name__ == "__main__":
	load_unities()
	load_buildings()
	load_salons()
