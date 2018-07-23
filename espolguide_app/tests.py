from django.test import TestCase, Client
from .views import *
from django.test import RequestFactory, TestCase
from .models import Users, Buildings, Favorites
# Create your tests here.

class CasoTest(TestCase):
    

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        user = Users(username="usuario_prueba", password="usuario_prueba", token="usuario_prueba1")
        user.save()
        self.client = Client(HTTP_ACCESS_TOKEN="usuario_prueba1")
        user2 = Users(username="usuario_prueba_2", password="usuario_prueba_2", token="usuario_prueba2")
        user2.save()
        user2_id = user2.id
        buildings = ["BLOQUE 32A","BLOQUE 32D", "BLOQUE 24A", "BLOQUE 32B", "BLOQUE 31B"]
        for building in buildings:
            building_obj = Buildings.objects.filter(code_gtsi=building)
            fav = Favorites(id_buildings = building_obj[0],id_users=user2_id)
            fav.save()
        self.clientFull = Client(HTTP_ACCESS_TOKEN="usuario_prueba2")

    def obtain_buildings_test(self):
        """Tests that the service returns the information and geometry of all the buildings"""
        request = self.factory.get('/obtainBuildings')
        response = obtain_buildings(request)
        self.assertEqual(response.status_code, 200)

    def obtain_buildings_info_test(self):
        """Tests that the service returns the information of all the buildings"""
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
        response = self.client.post('/buildingInfo/BLOQUE 32D/', {})
        json_response = response.json()
        expected_result = {}
        self.assertEqual(json_response, expected_result)
        
    def alternative_names_test(self):
        """Tests that the alternative names of all the buildings are returned"""
        request = self.factory.get('/alternativeNames')
        self.assertEqual(response.status_code, 200)

    def login_test(self):
        """Tests that a user can be created, given a username"""
        response = self.client.post('/login/', {'data': {'username': "usuario_prueba_1"}})
        self.assertEqual(response.status_code, 200)

    def token_user_test(self):
        """Tests that, given a username, it returns its respective token"""
        response = self.factory.get('/apitokenauth/usuario_prueba_1')
        self.assertEqual(response.status_code, 200)

    def get_building_centroid(self):
        """Tests that, given a gtsi_code=BLOQUE 15A, it returns the correct coordinates 
        of its centroid lat:-2.14716904758766, long:-79.96780304424358 """
        response = self.factory.get('/coordinates/BLOQUE 15A')
        expected_result = {'lat':-2.14716904758766,'long':-79.96780304424358}
        self.assertEqual(response.json(), expected_result)

    def show_photo_test(self):
        """Tests that, given a code_gtsi of a building, a photo of the building is returned"""
        response = self.factory.get('/photoBlock/BLOQUE 15A')
        self.assertEqual(response.status_code, 200)

    def add_favorites_test(self):
        """Tests that, given a code_gtsi code of a building and a token of a user, the service 
        adds the building to the list of favorites of the user, and returns the list"""
        response = self.client.post('/favorites/', {'code_gtsi':"BLOQUE 15A"})
        favs = ["BLOQUE 15A"]
        expected_result = {"code_gtsi":favs}
        self.assertEqual(response.json(), expected_result)

    def get_favorites_test(self):
        """Tests that, given the token of the user, the service returns the list of favorite pois 
        of the user"""
        response = self.client.get('/favorites/')
        favs = ["BLOQUE 15A"]
        expected_result = {"code_gtsi":favs}
        self.assertEqual(response.json(), expected_result)

    def add_6th_favorite_test(self):
        """Tests that, given a code_gtsi code of a building and a token of a user, 
        and that the user already has 5 favorite POIs, the service adds the building to the list 
        of favorites of the user, and returns the list"""
        response = self.client.post('/favorites/', {'code_gtsi':"BLOQUE 15A"})