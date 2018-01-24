'''Script para cargar shapefiles en la base de datos se debe ejecutar en el shell de django'''
import os
from django.contrib.gis.utils import LayerMapping
from .models import Bloques
# Auto-generated `LayerMapping` dictionary for Bloques model
BLOQUES_MAPPING = {
    'codigo': 'CODIGO',
    'nombre': 'NOMBRE',
    'unidad': 'UNIDAD',
    'bloque': 'BLOQUE',
    'tipo': 'TIPO',
    'descripcio': 'DESCRIPCIO',
    'area_m2': 'AREA_M2',
    'geom': 'MULTIPOLYGON',
}
BLOQUES_SHP = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'data/Bloques', 'BLOQUES_INGENIERIA.shp'),)


def run(verbose=True):
    '''Funcion para cargar los shapefiles'''
    layer_map = LayerMapping(
        Bloques, BLOQUES_SHP, BLOQUES_MAPPING,
        transform=False, encoding='iso-8859-1',
    )
    layer_map.save(strict=True, verbose=verbose)
