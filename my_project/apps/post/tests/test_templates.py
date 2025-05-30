from django.test import SimpleTestCase, TestCase
from django.urls import reverse

class AllPostsPageTest(TestCase):

	def test_url_exists_at_correct_location(self):
		response = self.client.get('/allposts/')
		self.assertEqual(response.status_code, 200)


	def test_url_available_by_name(self):
		response = self.client.get(reverse('user:apost'))
		self.assertEqual(response.status_code, 200)

	def test_template_name_correct(self):
		response = self.client.get(reverse('user:apost'))
		self.assertTemplateUsed(response, 'user/allposts.html')


	def test_template_content(self):
		response = self.client.get(reverse('user:apost'))
		self.assertContains(response, '<h1>You are not Logged In !!!</h1>')


class FriendPostsPageTest(SimpleTestCase):

	def test_url_exists_at_correct_location(self):
		response = self.client.get('/post/fposts/')
		self.assertEqual(response.status_code, 200)


	def test_url_available_by_name(self):
		response = self.client.get(reverse('post:fpost'))
		self.assertEqual(response.status_code, 200)


	def test_template_name_correct(self):
		response = self.client.get(reverse('post:fpost'))
		self.assertTemplateUsed(response, 'post/friends_post.html')


	def test_template_content(self):
		response = self.client.get('/post/fposts/')
		self.assertContains(response, '<h1>You are not Logged In !!!</h1>')


# class MyPostsPageTest(SimpleTestCase):

# 	def test_url_exists_at_correct_location(self):
# 		response = self.client.get('/post/m/')
# 		self.assertEqual(response.status_code, 200)


# 	def test_url_available_by_name(self):
# 		response = self.client.get(reverse('post:fpost'))
# 		self.assertEqual(response.status_code, 200)


# 	def test_template_name_correct(self):
# 		response = self.client.get(reverse('post:fpost'))
# 		self.assertTemplateUsed(response, 'post/friends_post.html')


# 	def test_template_content(self):
# 		response = self.client.get('/post/fposts/')
# 		self.assertContains(response, '<h1>You are not Logged In !!!</h1>')
		