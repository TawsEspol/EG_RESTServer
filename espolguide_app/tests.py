from django.test import TestCase, Client
from espolguide_app.views import *
from django.test import RequestFactory, TestCase
from espolguide_app.models import Users, Buildings, Favorites
from django.core.management import call_command
import os
import espolguide_app.loaddata_2019 as loaddata_2019
script_dir = os.path.dirname(__file__)

class CasoTest(TestCase):
    

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        #user to test the test_add_favorite
        user = Users(username="usuario_prueba", password="usuario_prueba", token="usuario_prueba1")
        user.save()
        self.client = Client(HTTP_ACCESS_TOKEN="usuario_prueba1")
        #user to test the add_6th_favorite_test
        user2 = Users(username="usuario_prueba_2", password="usuario_prueba_2", token="usuario_prueba2")
        user2.save()
        user2_id = user2.id
        loaddata_2019.run()
        buildings = ["11A","11B", "11C", "11D", "6A"]
        for building in buildings:
            building_obj = Buildings.objects.filter(code_gtsi=building)
            fav = Favorites(id_buildings = building_obj[0],id_users=user2)
            fav.save()
        self.clientFull = Client(HTTP_ACCESS_TOKEN="usuario_prueba2")

    def test_obtain_buildings(self):
        """Tests that the service returns the information and geometry of all the buildings"""
        request = self.factory.get('/obtainBuildings')
        response = obtain_buildings(request)
        self.assertEqual(response.status_code, 200)

    def test_obtain_buildings_info(self):
        """Tests that the service returns the information of all the buildings"""
        request = self.factory.get('/obtainBuildingsInfo')
        response = obtain_buildings_info(request)
        self.assertEqual(response.status_code, 200)
        
    def test_alternative_names(self):
        """Tests that the alternative names of all the buildings are returned"""
        request = self.factory.get('/alternativeNames')
        response = alternative_names(request)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Tests that, given a username, their data is returned"""
        python_dict = {"data": {"username": "usuario_prueba_2"}}
        response = self.client.post('/login/', json.dumps(python_dict), content_type="application/json")
        datos = response.json()
        #we do not know what token is generated, but the correct behaviour should be that the endpoint retunrs 
        #a json with 1 key called "access-token"
        #so we check that the returned json has a length of 1
        self.assertEqual(len(datos),1)

    def test_login_no_user(self):
        """Tests that a user can be created"""
        python_dict = {"data": {"username": "new_user"}}
        response = self.client.post('/login/', json.dumps(python_dict), content_type="application/json")
        datos = response.json()
        self.assertEqual(len(datos),1)

    def test_token_user(self):
        """Tests that, given a username, its token auth regenerates"""
        response = self.client.get('/apitokenauth/usuario_prueba_2')
        datos = response.json()
        self.assertEqual(len(datos),1)

    def test_get_building_centroid(self):
        """Tests that, given a gtsi_code=11A, it returns the correct coordinates 
        of its centroid lat:-2.14716904758766, long:-79.96780304424358 """
        python_dict = {"code_gtsi": "11A", "code_infra":"11A"}
        response = self.client.post('/coordinates/', json.dumps(python_dict), content_type="application/json")
        response = response.json()
        expected_result = {'lat':-2.1446204723353177,'long':-79.96768222340235}
        result = response["lat"]==expected_result["lat"] and response["long"]==expected_result["long"]
        self.assertEqual(result, True)

    def test_show_photo(self):
        """Tests that, given a code_gtsi of a building, a photo of the building is returned"""
        response = self.client.get('/photoBlock/11A')
        self.assertEqual(response.status_code, 302)


    def test_add_favorites(self):
        """Tests that, given a code_gtsi code of a building and a token of a user, the service 
        adds the building to the list of favorites of the user, and returns the list"""
        python_dict = {"code_gtsi": "6B", "code_infra":"6B"}
        response = self.client.post('/favorites/', json.dumps(python_dict), content_type="application/json")
        favs = ["6B"]
        response = response.json()
        expected_result = {"codes_gtsi":favs,"codes_infra":["6B"]}
        self.assertEqual(response, expected_result)

    def test_get_favorites(self):
        """Tests that, given the token of the user, the service returns the list of favorite pois 
        of the user"""
        response = self.client.get('/favorites/')
        favs = []
        expected_result = {"codes_gtsi":favs,"codes_infra":favs}
        self.assertEqual(response.json(), expected_result)

    def test_add_6th_favorite(self):
        """Tests that, given a code_gtsi code of a building and a token of a user, 
        and that the user already has 5 favorite POIs, the service adds the building to the list 
        of favorites of the user, and returns the list"""
        self.client = Client(HTTP_ACCESS_TOKEN="usuario_prueba2")
        python_dict = {"code_gtsi": "6B", "code_infra":"6B"}
        response = self.client.post('/favorites/', json.dumps(python_dict), content_type="application/json")
        response = response.json()
        #Check if the user has no more than 5 favorite pois and that BLOQUE 15A is in his favorites
        returned_result = len(response["codes_gtsi"]) == 5 and "6B" in response["codes_gtsi"]
        self.assertEqual(returned_result, True)

