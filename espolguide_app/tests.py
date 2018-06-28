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

    def add_user_test(self):
        # Create an instance of a GET request.
        request = self.factory.get('/photoBlock/16-C')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = show_photo(request)
        self.assertEqual(response.status_code, 200)
