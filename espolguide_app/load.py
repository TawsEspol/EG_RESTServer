import os
from django.contrib.gis.utils import LayerMapping
from .models import Bloques
# Auto-generated `LayerMapping` dictionary for Bloques model
bloques_mapping = {
    'codigo' : 'CODIGO',
    'nombre' : 'NOMBRE',
    'unidad' : 'UNIDAD',
    'bloque' : 'BLOQUE',
    'tipo' : 'TIPO',
    'descripcio' : 'DESCRIPCIO',
    'area_m2' : 'AREA_M2',
    'geom' : 'MULTIPOLYGON',
}
bloques_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data/Bloques', 'BLOQUES_INGENIERIA.shp'),
)

def run(verbose=True):
    lm = LayerMapping(
        Bloques, bloques_shp, bloques_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)
