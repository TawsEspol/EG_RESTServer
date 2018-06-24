from django.test import TestCase
from .views import *


# Create your tests here.

class CasoTest(TestCase):
    
    def test_views(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(info_bloque(primary_key = 1),'{"features": [{"geometry":\
         {"coordinates": [[[-2.14537420416497, -79.9651225218215]]], "type": "Polygon"}, \
         "properties": {"nombre": "Decanato", "codigo": "19", "descripcio": "Gobierno de FICT", "tipo":\
          "Edificio", "unidad": "FICT", "bloque": "19"}, "type": "Feature"}], "type": "FeatureCollection"}')

