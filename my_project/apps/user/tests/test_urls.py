from django.test import SimpleTestCase
from django.urls import reverse

class ForgotPasswordUrlsTest(SimpleTestCase):

	def test_url_exists_at_correct_location(self):
		response = self.client.get('/fpass/')
		self.assertEqual(response.status_code, 200)

	def test_url_available_by_name(self):
		response = self.client.get(reverse('user:forgotpass'))
		self.assertEqual(response.status_code, 200)


	def test_template_name_correct(self):
		response = self.client.get(reverse('user:forgotpass'))
		self.assertTemplateUsed(response, 'user/fpass.html')


	def test_template_content(self):
		response = self.client.get(reverse('user:forgotpass'))
		self.assertContains(response, 'Find Your Account')