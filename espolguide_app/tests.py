from django.test import TestCase, Client
from .views import *
from django.test import RequestFactory, TestCase

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

    def building_info_bad_token_test(self):
        """Tests that given an existent username and an invalid token, and the code of the building,
         the endpoint returns an empty json object """
        token = ""
        request = self.factory.get('/buildingInfo/BLOQUE 32D/'+token)
        response = building_info(request)
        self.assertEqual(response.status_code, 200)

    def building_info_test(self):
        """Tests that given an existent username and an valid token, and the code of the building,
         the endpoint returns the information of a building in a json object """
        c = Client()
        response = c.post('/buildingInfo/BLOQUE 32D/', {})
        json_response = response.json()
        expected_result = {}
        self.assertEqual(json_response, expected_result)
        
    def get_building_centroid_test(self):
        request = self.factory.get('/coordinates/BLOQUE 32D/')
        self.assertEqual(response.status_code, 200)

    def alternative_names_test(self):
        request = self.factory.get('/alternativeNames')
        self.assertEqual(response.status_code, 200)

    
