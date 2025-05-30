from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from faker import Faker
# Using the standard RequestFactory API to create a form POST request
# factory = APIRequestFactory()
# request = factory.post(reverse('/api/'), {'title': 'new idea'})

# # Using the standard RequestFactory API to encode JSON data
# request = factory.post('/notes/', {'title': 'new idea'}, content_type='application/json')


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse("create_apiuser")
        self.login_url = reverse("login_apiuser")
        self.fake = Faker()
        self.user_data = {
            'username': self.fake.first_name(),
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': self.fake.email(),
            'password': 'Test@12345',
            're_password': 'Test@12345',
            'contact': '1234569870'
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()