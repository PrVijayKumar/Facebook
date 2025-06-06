from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.http import HttpRequest
from user.views import login
from ipware import get_client_ip
from django.urls import reverse
from user.signals import request_by_user
CustomUser = get_user_model()


class LoginTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")

    def test_login_failed(self):
        response = self.client.login(username=self.user.username, password="1234")
        self.assertIsNotNone(self.user)
        self.assertFalse(response)


    def test_log_out(self):
        self.client.login(username=self.user.username, password="@@123456")
        response = self.client.logout()
        self.assertIsNone(response)

    @patch('user.receivers.get_client_ip')
    def test_is_routable_ip_signals(self, mock_cl_ip):
        mock_cl_ip.return_value = '127.0.0.1', True
        request = HttpRequest()
        request_by_user.send(sender=CustomUser, username=self.user.username, request=request)
        mock_cl_ip.assert_called_once()



    # @patch("user.receivers.log_ip.is_routable")
    # @patch("user.receivers.get_client_ip")
    # @patch('user.views.messages')
    # def test_is_routable_ip_signals(self, mock_cl_ip):
    #     mock_cl_ip.return_value = "127.0.0.1", True
    #     # mock_is_routable = True
    #     # response = self.client.login(username=self.user.username, password="@@123456")
    #     response = self.client.post(request)
    #     # mock_cl_ip.assert_called_once_with()
    #     print(self.client.request)
    #     mock_cl_ip.assert_called_once_with(self.client.request)
    #     self.assertTrue(response)
    # @patch('user.views.authenticate')
    # @patch('user.views.auth_login')
        # mock_cl_ip.assert_called_once_with(self.user.username)
        
        # request.POST['username'] = self.user.username
        # request.POST['password'] = "123456"
        # request.method = 'POST'
        # mock_user = mock_authenticate.return_value
        # response = self.client.login(username=self.user.username, password="123")
        # login(request)