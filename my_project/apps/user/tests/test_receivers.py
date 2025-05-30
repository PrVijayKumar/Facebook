from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from ipware import get_client_ip
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

    # @patch("user.receivers.log_ip.is_routable")
    @patch("user.receivers.get_client_ip")
    def test_is_routable_ip_signals(self, mock_cl_ip):
        mock_cl_ip.return_value = "127.0.0.1", True
        # mock_is_routable = True
        response = self.client.login(username=self.user.username, password="@@123456")
        # mock_cl_ip.assert_called_once_with()
        print(self.client.request)
        # mock_cl_ip.assert_called_once_with(self.client.request)
        self.assertTrue(response)
        