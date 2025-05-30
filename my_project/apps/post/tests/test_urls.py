from django.test import SimpleTestCase
from post.models import PostModel, PostComments, PostLikes
from user.models import CustomUser


class PostTemplateTest(SimpleTestCase):

	# set Up Function


	# test url exists at correct location
	def test_urls_with_get_request(self):
		# self.assertEqual(self.client.get('/post/allposts/').status_code, 200)
		# self.assertEqual(self.client.get('/post/myposts/').status_code, 200)
		self.assertEqual(self.client.get('/post/fposts/').status_code, 200)
		self.assertEqual(self.client.get('/myposts/edit/1').status_code, 404)
		self.assertEqual(self.client.get('/myposts/dpost/1').status_code, 404)
		self.assertEqual(self.client.get('/lpost/1').status_code, 404)
		self.assertEqual(self.client.get('/comments/1').status_code, 404)
		self.assertEqual(self.client.get('/fcomments/1').status_code, 404)
		self.assertEqual(self.client.get('/freplies/1').status_code, 404)
		self.assertEqual(self.client.get('/cedit/1').status_code, 404)
		self.assertEqual(self.client.get('/cdelete/1').status_code, 404)
		

