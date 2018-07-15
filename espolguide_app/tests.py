from django.test import TestCase
from .views import *
from django.test import RequestFactory, TestCase
from .models import User
from .views import add_user, token_user, show_photo

# Create your tests here.

class CasoTest(TestCase):
    

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        #self.user = User(username="usuario_prueba")

    def obtain_buildings_test(self):
        request = self.factory.get('/obtainBuildings')
        response = obtain_buildings(request)
        self.assertEqual(response.status_code, 200)

    def obtain_buildings_info_test(self):
        request = self.factory.get('/obtainBuildingsInfo')
        response = obtain_buildings_info(request)
        self.assertEqual(response.status_code, 200)

    def building_info_test(self):
        token = self.factory.get('/apitokenauth/usuario_prueba_1')
        request = self.factory.get('/buildingInfo/BLOQUE 32D/'+token)
        self.assertEqual(response.status_code, 200)

    def get_building_centroid_test(self):
        request = self.factory.get('/coordinates/BLOQUE 32D/')
        self.assertEqual(response.status_code, 200)

    def alternative_names_test(self):
        request = self.factory.get('/alternativeNames')
        self.assertEqual(response.status_code, 200)

    
