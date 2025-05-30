from django.test import SimpleTestCase
from django.urls import reverse

# import unittest

class LoginPageTests(SimpleTestCase):

	def test_url_exists_at_correct_location(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)


	def test_url_available_by_name(self):
		response = self.client.get(reverse('user:login-page'))
		self.assertEqual(response.status_code, 200)


	def test_template_name_correct(self):
		response = self.client.get(reverse('user:login-page'))
		self.assertTemplateUsed(response, "user/login.html")


	def test_template_content(self):
		response = self.client.get(reverse('user:login-page'))
		self.assertContains(response, "Login")


class RegisterPageTests(SimpleTestCase):

	def test_url_exists_at_correct_location(self):
		response = self.client.get("/register/")
		self.assertEqual(response.status_code, 200)


	def test_url_available_by_name(self):
		response = self.client.get(reverse('user:register'))
		self.assertEqual(response.status_code, 200)


	def test_template_name_correct(self):
		response = self.client.get(reverse('user:register'))
		self.assertTemplateUsed(response, "user/register.html")

	def test_template_content(self):
		response = self.client.get(reverse('user:register'))
		self.assertContains(response, "Create a new account")


# class AppPostsPageTests(SimpleTestCase):

# 	def test_url_exists_at_correct_location(self):
# 		response = self.client.post("/allposts/")
# 		self.assertEqual(response.status_code, 200)


	# def test_url_available_by_name(self):
	# 	reponse = self.client.get(reverse('user:apost'))
	# 	self.assertEqual(respone.status_code, 200)


	# def test_template_name_correct(self):
	# 	response = self.client.get(reverse('user:apost'))
	# 	self.assertTemplateUsed(resposne, "user/allposts.html")


