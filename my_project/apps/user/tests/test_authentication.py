from django.test import TestCase
from user.models import CustomUser
from django.urls import reverse
from unittest.mock import Mock, patch
from django.contrib.auth import authenticate, get_user_model, SESSION_KEY
from django.http import HttpRequest
from user.views import login
from django.contrib import messages
from django.contrib.auth import login as auth_login
from user.customauth import CustomAuthentication

class BaseTest(TestCase):

	# define set up function
	def setUp(self):
		self.register_url = reverse('user:register')
		self.user = {
			'username': 'testusername',
			'first_name': 'testfirstname',
			'last_name': 'testlastname',
			'email': 'testemail@gmail.com',
			'password1': 'Test@@123456',
			'password2': 'Test@@123456',
			'contact': '1234567890',
			'dob_month': '5',
			'dob_day': '1',
			'dob_year': '1980'
		}
		self.user_shortpass = {
			'username': 'testusername',
			'first_name': 'testfirstname',
			'last_name': 'testlastname',
			'email': 'testemail@gmail.com',
			'password1': 'Test@@',
			'password2': 'Test@@',
			'contact': '1234567890',
			'dob_month': '5',
			'dob_day': '1',
			'dob_year': '1980'
		}
		self.user_unmatchingpassword = {
			'username': 'testusername',
			'first_name': 'testfirstname',
			'last_name': 'testlastname',
			'email': 'testemail@gmail.com',
			'password1': 'Test@@123456',
			'password2': 'Test@@12345678',
			'contact': '1234567890',
			'dob_month': '5',
			'dob_day': '1',
			'dob_year': '1980'
		}
		self.user_invalid_email = {
			'username': 'testusername',
			'first_name': 'testfirstname',
			'last_name': 'testlastname',
			'email': 'test.com',
			'password1': 'Test@@12345678',
			'password2': 'Test@@12345678',
			'contact': '1234567890',
			'dob_month': '5',
			'dob_day': '1',
			'dob_year': '1980'
		}
		return super().setUp()



class RegisterTest(BaseTest):

	# test can view page correctly
	def test_can_view_page_correctly(self):
		response = self.client.get(self.register_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/register.html')


	# test register user
	def test_can_register_user(self):
		response = self.client.post(self.register_url, self.user, format='text/html')
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, 'user/login.html')


	# test can't register with short password
	def test_cant_register_with_short_password(self):
		response = self.client.post(self.register_url, self.user_shortpass, format='text/html')
		self.assertEqual(response.status_code, 200)
		# self.assertContains(response, 'This password is too short. It must contain at least 8 characters.')


	# test can't register users with unmatching passwords
	def test_cant_register_user_with_unmatching_password(self):
		response = self.client.post(self.register_url, self.user_unmatchingpassword, format='text/html')
		self.assertEqual(response.status_code, 200)

	# test can't register user with invalid email
	def test_cant_register_user_with_invalid_email(self):
		response = self.client.post(self.register_url, self.user_invalid_email, format='text/html')
		self.assertEqual(response.status_code, 200)

	# test can't register user with taken email
	def test_cant_register_user_with_taken_email(self):
		self.client.post(self.register_url, self.user_invalid_email, format='text/html')
		response = self.client.post(self.register_url, self.user_invalid_email, format='text/html')
		self.assertEqual(response.status_code, 200)


class LogInTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	# test the login page
	# @patch('django.contrib.auth.authenticate')
	@patch('user.views.authenticate')
	def test_login(self, mock_authenticate):
		mock_authenticate.return_value = None
		# response = self.client.post(reverse('user:login-page'), {'assertion': 'assert this'})
		# mock_authenticate.assert_called_once_with(assertion='assert this')
		response = self.client.post(reverse('user:login-page'), self.credentials)
		mock_authenticate.assert_called_once_with(username=self.credentials['username'], password=self.credentials['password'])
		# response = self.client.post(reverse('user:login-page'), self.credentials, format='text/html')
		# response = self.client.login(username=self.credentials['username'], password=self.credentials['password'])
		# breakpoint()
		# mock_authenticate.assert_called_once_with(self.credentials, format='text/html')
		# self.assertTrue(response.context['user'].is_authenticated)


	@patch('user.views.authenticate')
	def test_returns_OK_when_user_found(self, mock_authenticate):
		user = self.user
		user.backend = '' # required for auth_login to work
		mock_authenticate.return_value = user
		response = self.client.post(reverse('user:login-page'), self.credentials)
		# breakpoint()
		# self.assertEqual(response.content.decode(), 'OK')
		# breakpoint()
		self.assertEqual(response.status_code, 302)



	# test to check logged in session if authenticate returns a user
	@patch('user.views.authenticate')
	def test_gets_logged_in_session_if_authenticate_returns_user(self, mock_authenticate):
		user = self.user
		user.backend = ''
		mock_authenticate.return_value = user
		response = self.client.post(reverse('user:login-page'), self.credentials)
		self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))


	# test to check to not to log in if authenticate returns a None
	@patch('user.views.authenticate')
	def test_does_not_get_logged_in_session_if_authenticate_returns_None(self, mock_authenticate):
		user = self.user
		user.backend = ''
		mock_authenticate.return_value = None
		response = self.client.post(reverse('user:login-page'), self.credentials)
		self.assertNotIn(SESSION_KEY, self.client.session)



	# test to check login with request and without test client
	@patch('user.views.messages')
	@patch('user.views.auth_login')
	@patch('user.views.authenticate')
	def test_calls_auth_login_if_authenticate_returns_a_user(self, mock_authenticate, mock_login, mock_messages):
		request = HttpRequest()
		request.POST['username'] = self.credentials['username']
		request.POST['password'] = self.credentials['password']
		request.method = 'POST'
		mock_user = mock_authenticate.return_value
		login(request)
		mock_login.assert_called_once_with(request, mock_user)



# test for custom authentication
class AuthenticateTest(TestCase):

	# set Up Test Data
	@classmethod
	def setUpTestData(cls):
		cls.backend = CustomAuthentication()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}

	# tests returns None if response errors
	def test_returns_none_if_response_errors(self):

		user = self.backend.authenticate()
		self.assertIsNone(user)


	# test finds existing user with email
	def test_finds_existing_user_with_email(self):
		actual_user = self.user
		found_user = self.backend.authenticate(username=actual_user.email, password="@@123456")
		self.assertEqual(actual_user, found_user)


	# test return none if no user with that email
	def test_returns_none_if_no_user_with_that_email(self):
		user = self.backend.authenticate(username='salman@gmail.com', password='@@123456')
		self.assertIsNone(user)


	# test finds existing user with username
	def test_finds_existing_user_with_username(self):
		actual_user = self.user
		found_user = self.backend.authenticate(username=actual_user.username, password="@@123456")
		self.assertEqual(actual_user, found_user)


	# test finds existing user with contact
	def test_finds_existing_user_with_contact(self):
		actual_user = self.user
		found_user = self.backend.authenticate(username=actual_user.contact, password="@@123456")
		self.assertEqual(actual_user, found_user)


	# test returns none with wrong password
	def test_returns_none_with_wrong_password(self):
		user = self.backend.authenticate(username=self.user.email, password="@@12345678")
		self.assertIsNone(user)



class GetUserTest(TestCase):

	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.backend = CustomAuthentication()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}



	# test getting user with user id
	def test_gets_user_by_id(self):
		actual_user = self.user
		found_user = self.backend.get_user(self.user.id)
		self.assertEqual(actual_user, found_user)

	# test getting none if any error occurs
	def test_returns_none_if_no_user_with_user_that_id(self):
		self.assertIsNone(
			self.backend.get_user(1000000) # passing wrong id
		)

class LogOutTest(TestCase):
	
	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.backend = CustomAuthentication()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}

	# test to login and logout a user
	# @patch('user.views.messages')
	# @patch('user.views.auth_logout')
	# @patch('user.views.auth_login')
	# @patch('user.views.authenticate')
	# def test_to_login_logout_user(self, mock_authenticate, mock_login, mock_logout, mock_messages):
	# 	user = self.user
	# 	mock_authenticate.return_value = user
	# 	response = self.client.post(reverse())

	# testing logout
	def test_logout(self):
		response = self.client.post(reverse('user:logout'))
		self.assertEqual(response.status_code, 302)

	# follow redirect
	def test_logout_redirect(self):
		response = self.client.post(reverse('user:logout'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/login.html')
		self.assertContains(response, 'Login')