from django.test import TestCase
from django.test.client import MULTIPART_CONTENT
from post.models import PostModel, PostComments, PostLikes
from user.models import CustomUser
from django.utils import timezone
from django.urls import reverse
import pathlib
from django.core.files.uploadedfile import SimpleUploadedFile


class PostTest(TestCase):

	@classmethod
	def setUpClass(cls):
		super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		# self.client.login(username=self.credentials['username'], password="@@123456")
		pass



	# test model content
	def test_model_content(self):
		self.assertEqual(self.post.post_title, "Test Post")
		# self.assertEqual(self.post.post_user, "shah@gmail.com")
		self.assertEqual(self.post.post_user.id, self.user.id)
		self.assertEqual(self.post.post_description, "This post is created for testing purpose.")
		self.assertEqual(self.post.post_content, "images/yellowcar.webp")
		self.assertEqual(str(self.post.post_date.date()), str(timezone.now().date()))
		self.assertEqual(self.post.post_likes, 0)


	# test url exists at correct location
	def test_url_exists_at_correct_location(self):
		response = self.client.get("/allposts/")
		self.assertEqual(response.status_code, 200)


	# test url available by name
	def test_url_available_by_name(self):
		response = self.client.get(reverse('user:apost'))
		self.assertEqual(response.status_code, 200)		


	# test template name correct
	def test_template_name_correct(self):
		response = self.client.get(reverse('user:apost'))
		self.assertTemplateUsed(response, 'user/allposts.html')

	# test template name correct with post request
	def test_template_name_correct_with_post_request(self):
		response = self.client.post(reverse('user:apost'))
		


	# test template content
	def test_template_content(self):
		response = self.client.get(reverse('user:apost'))
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")
		response = self.client.post(reverse('user:apost'),
			{
				'username': 'shah@gmail.com',
				'password': '@@123456',
			}
			)
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")



class CreatePostTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass

	# test create post create view when logged in and get request
	def test_create_post_view_get(self):

		self.client.login(username=self.credentials['username'], password="@@123456")
		# test for get request
		response = self.client.get(reverse("post:cpost"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/createpost.html")
		self.assertContains(response, "Create Post")


	# test create post create view when not logged in and post request
	def test_create_post_view_post(self):

		self.client.login(username=self.credentials['username'], password="@@123456")
		path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
		myimg = open(path, 'rb')
		f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")

		response = self.client.post(reverse("post:cpost"), {
			'title': 'Test Post 2',
			'description': 'Post Description about test',
			'content': f
		})
		posts = PostModel.objects.filter(post_user=self.user)
		for p in posts:
			print(p.post_content) 
		self.assertIsNotNone(self.user.postname)
		self.assertEqual(response.status_code, 302)
		# test for get request
		# path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media'
		# breakpoint()
		# print(path)
		# , format="multipart"
		# }, content_type=MULTIPART_CONTENT)
		# self.assertTemplateUsed(response, "post/createpost.html")
		# self.assertContains(response, "Create Post")
		# print(path)
		# using context manager
		# with open(path, 'rb').read() as myimg:
		# myimage = open(path,'r', encoding='utf-8')
		# f = SimpleUploadedFile("birthday.jpegmy", b"path", content_type='image/jpg')
			# 'content': "images/yellowcar.webp",


	# test create post create view when not logged in and post request follow redirect
	def test_create_post_view_post_fr(self):

		self.client.login(username=self.credentials['username'], password="@@123456")
		path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
		myimg = open(path, 'rb')
		f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")

		response = self.client.post(reverse("post:cpost"), {
			'title': 'Test Post',
			'description': 'Post Description about test',
			'content': f
		}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/allposts.html")
		self.assertContains(response, f"Hello, {self.user.first_name}")
	
	
	# test create post create view when logged in and get request
	def test_create_post_view_get_nl(self):

		# test for get request
		response = self.client.get(reverse("post:cpost"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/createpost.html")
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")


	# test create post create view when logged in and get request
	def test_create_post_view_post_nl(self):
		
		path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
		myimg = open(path, 'rb')
		f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")

		response = self.client.post(reverse("post:cpost"), {
			'title': 'Test Post',
			'description': 'Post Description about test',
			'content': f
		})

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/createpost.html")
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")



class MyPostTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test mypost view with get request when not logged in
	def test_my_post_view_get_nl(self):

		# test for get request
		response = self.client.get(reverse("post:mpost"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/myposts.html")
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")


	# test mypost view with get request when logged in
	def test_my_post_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		# test for get request
		response = self.client.get(reverse("post:mpost"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/myposts.html")
		self.assertContains(response, "My Posts")



# class AllPostsTest(TestCase):
	
# 	@classmethod
# 	def setUpTestData(cls):
# 		# super(PostTest, cls).setUpClass()
# 		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
# 			dob="2000-04-29")
# 		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
# 			post_content="images/yellowcar.webp")
# 		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)
# 		cls.credentials = {
# 			'username': 'shah@gmail.com',
# 			'password': '@@123456'
# 		}


# 	def setUp(self):
# 		pass


# 	# test allpost view with get request when not logged in
# 	def test_all_posts_view_get_nl(self):

# 		# test for get request
# 		response = self.client.get(reverse("post:apost"))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, "post/allposts.html")
# 		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")


# 	# test allpost view with get request when logged in
# 	def test_all_post_view_get(self):
# 		self.client.login(username=self.credentials['username'], password="@@123456")

# 		# test for get request
# 		response = self.client.get(reverse("post:apost"))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, "post/allposts.html")
# 		# self.assertContains(response, "My Posts")


class FriendsPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test friends post view with get request when not logged in
	def test_friends_post_view_get_nl(self):
		response = self.client.get(reverse("post:fpost"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/friends_post.html")
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")


	# test friends view with get request when logged in
	def test_friends_post_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:fpost"))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/friends_post.html")
		self.assertContains(response, "Friends Posts")



class DetailPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test allfriends post view with get request when not logged in
	def test_friends_post_view_get_nl(self):
		response = self.client.get(reverse("post:detpost", kwargs={'id': self.post.id}))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/detpost.html")
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")


	# test friends post view with get request when logged in
	def test_friends_post_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:detpost", kwargs={'id': self.post.id}))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "post/detpost.html")
		self.assertContains(response, "")

class DeletePostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test delete view with get request when not logged in
	def test_del_post_view_get_nl(self):
		response = self.client.get(reverse("post:dpost", kwargs={'id': self.post.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test delete view with get request when not logged in and follow redirect
	def test_del_post_view_get_nl_fr(self):
		response = self.client.get(reverse("post:dpost", kwargs={'id': self.post.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test delete view with get request when logged in and follow redirect
	def test_friends_post_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:dpost", kwargs={'id': self.post.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "deleted")
		self.assertJSONEqual( 
			response_content,
			{'result': '{"result": "Deleted", "id": "'+str(self.post.id)+'", "msg": "Post Deleted"}'}
		)


	# test delete view with post request when logged in and follow redirect
	def test_friends_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.post(reverse("post:dpost", kwargs={'id': self.post.id}), content_type='application/json',
    				HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# print(response.content)
		response_content = str(response.content, encoding='utf8')
		self.assertContains(response, "Deleted")
		self.assertJSONEqual( 
			response_content,
			{'result': '{"result": "Deleted", "id": "'+str(self.post.id)+'", "msg": "Post Deleted"}'}
		)






class LikePostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test like view with get request when not logged in
	def test_like_post_view_get_nl(self):
		response = self.client.get(reverse("post:lpost", kwargs={'id': self.post.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test like view with get request when not logged in and follow redirect
	def test_like_post_view_get_nl_fr(self):
		response = self.client.get(reverse("post:lpost", kwargs={'id': self.post.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test like view with get request when logged in
	def test_like_post_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:lpost", kwargs={'id': self.post.id}), HTTP_REFERER='https://localhost:8000/test')
		self.assertEqual(response.status_code, 302)
		# self.assertContains(response, "deleted")
		# self.assertJSONEqual( 
		# 	response_content,
		# 	{'result': '{"result": "Deleted", "id": "'+str(self.post.id)+'", "msg": "Post Deleted"}'}
		# )


	# test like with post request when logged in and follow redirect
	def test_like_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.post(reverse("post:lpost", kwargs={'id': self.post.id}), {'uid': self.user.id, 'flag': 1})
		# print(response)
		# response = self.client.get(reverse("post:lpost", kwargs={'id': self.post.id}), content_type='application/json',
    	# 			HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# print(response.content)
		# response_content = str(response.content, encoding='utf8')
		# self.assertContains(response, str(self.post.post_likes))
		# self.assertJSONEqual( 
		# 	response_content,
		# 	{'result': '{"result": "Deleted", "id": "'+str(self.post.id)+'", "msg": "Post Deleted"}'}
		# )
		

	# test dislike with post request when logged in and follow redirect
	def test_dislike_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		liked = self.client.post(reverse("post:lpost", kwargs={'id': self.post.id}), {'uid': self.user.id, 'flag': 1})
		response = self.client.post(reverse("post:lpost", kwargs={'id': self.post.id}), {'uid': self.user.id, 'flag': 0})
		# print(response)
		# response = self.client.get(reverse("post:lpost", kwargs={'id': self.post.id}), content_type='application/json',
    	# 			HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)





class EditPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test edit post view with get request when not logged in
	def test_edit_post_view_get_nl(self):
		response = self.client.get(reverse("post:epost", kwargs={'id': self.post.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test like view with get request when not logged in and follow redirect
	def test_edit_post_view_get_nl_fr(self):
		response = self.client.get(reverse("post:lpost", kwargs={'id': self.post.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test like view with get request when logged in
	def test_edit_post_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:lpost", kwargs={'id': self.post.id}), HTTP_REFERER='https://localhost:8000/test')
		self.assertEqual(response.status_code, 302)
		# self.assertContains(response, "deleted")
		# self.assertJSONEqual( 
		# 	response_content,
		# 	{'result': '{"result": "Deleted", "id": "'+str(self.post.id)+'", "msg": "Post Deleted"}'}
		# )


	# test edit post with post request when logged in and follow redirect
	def test_edit_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
		myimg = open(path, 'rb')
		f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")

		response = self.client.post(reverse("post:epost", kwargs={'id': self.post.id}), {
			'post_title': 'test updated',
			'post_description': 'test description updated',
			'post_content': f
			})
		self.assertEqual(response.status_code, 200)


		

	# test dislike with post request when logged in and invalid form
	def test_edit_post_view_get_invalid_form(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:epost", kwargs={'id': self.post.id}), {
			'post_title': 'test updated',
			'post_description': 'test description updated'
			})
		self.assertEqual(response.status_code, 200)



class CommentPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test comment post view with get request when not logged in
	def test_comment_post_view_get_nl(self):
		response = self.client.get(reverse("post:comment", kwargs={'id': self.post.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test comment view with get request when not logged in and follow redirect
	def test_comment_post_view_get_nl_fr(self):
		response = self.client.get(reverse("post:comment", kwargs={'id': self.post.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test comment view with get request when logged in
	def test_comment_post_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:comment", kwargs={'id': self.post.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertContains(response, "deleted")
		self.assertJSONEqual( 
			response_content,
			'{"result": "error"}'
		)


	# test comment post with post request when logged in and follow redirect
	def test_comment_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")


		response = self.client.post(reverse("post:comment", kwargs={'id': self.post.id}), {
			'comment_desc': 'test comment'
			})
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "object"}'
		# )

		

	# test comment with post request when logged in and invalid form
	def test_comment_post_view_post_invalid_form(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.post(reverse("post:comment", kwargs={'id': self.post.id}), {
			'comment_desc': ''
			})
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual( 
			response_content,
			'{"result": "error"}'
		)

	# test reply with post request when logged in and invalid form
	def test_reply_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		comment = PostComments.objects.create(comment_desc="Test Comment", post=self.post, com_user=self.user)
		# print(comment)
		response = self.client.post(reverse("post:comment", kwargs={'id': self.post.id}), {
			'comment_desc': 'Test Reply',
			'post': self.post,
			'com_reply': self.user.username,
			'reply_on_comment': comment.id
			})
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )

	# test comment with inappropriate words
	def test_comment_with_inappropriate_words(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		kw = {'id': self.post.id}
		url = reverse("post:comment", kwargs=kw)
		data = {
			'comment_desc': "Test Comment terrorism",
			'post': self.post,
			'com_user': self.user
			}
		# print(comment)
		# response = self.client.post(url, data)
		# response_content = str(response.content, encoding='utf8')
		# print(response_content)
		# self.assertEqual(response.status_code, 200)
		# self.assertEqual(response, "Inappropriate Comment")
		# self.assertRaises(Exception, pre_save_comments, "Inappropriate Comment")
		# self.assertRaises(ValueError("Inappropriate Comment"), self.client.post, (url, data))
		# with self.assertRaises(ValueError) as context:
		# 	self.client.post(url, data)
		# self.assertEqual(str(context.exception), 'Inappropriate Comment')

		with self.assertRaisesRegex(Exception, 'Inappropriate Comment'):
			self.client.post(url, data)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )




class FetchCommentPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.comment = PostComments.objects.create(comment_desc="Test Comment", post=cls.post, com_user=cls.user)
		cls.comment2 = PostComments.objects.create(comment_desc="Test Comment2", post=cls.post, com_user=cls.user)
		cls.reply = PostComments.objects.create(comment_desc="Test Reply", post=cls.post, com_user=cls.user, com_reply=cls.user, reply_on_comment=cls.comment.id)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test fetch comment view with get request when not logged in
	def test_fetch_comment_view_get_nl(self):
		response = self.client.get(reverse("post:fcomments", kwargs={'id': self.post.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test fetch comment with get request when not logged in and follow redirect
	def test_fetch_comment_view_get_nl_fr(self):
		response = self.client.get(reverse("post:fcomments", kwargs={'id': self.post.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test fetch comment view with get request when logged in
	def test_fetch_comment_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:fcomments", kwargs={'id': self.post.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# print(response_content)
		# self.assertContains(response, "deleted")
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )


	# test fetch comment view with get request when logged in
	def test_fetch_comment_when_no_comment_exist_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		PostComments.objects.all().delete()
		response = self.client.get(reverse("post:fcomments", kwargs={'id': self.post.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# print(response_content)
		# self.assertContains(response, "deleted")
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )


	# test fetch comment with post request when logged in and follow redirect
	def test_fetch_comment_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")


		response = self.client.post(reverse("post:fcomments", kwargs={'id': self.post.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "object"}'
		# )

		

	# test fetch comment with no replies post request when logged in
	def test_fetch_comment_with_no_reply_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.post(reverse("post:fcomments", kwargs={'id': self.post.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )

	# test reply with post request when logged in and invalid form
	# def test_reply_post_view_post(self):
	# 	self.client.login(username=self.credentials['username'], password="@@123456")
	# 	comment = PostComments.objects.create(comment_desc="Test Comment", post=self.post, com_user=self.user)
	# 	print(comment)
	# 	response = self.client.post(reverse("post:comment", kwargs={'id': self.post.id}), {
	# 		'comment_desc': 'Test Reply',
	# 		'post': self.post,
	# 		'com_reply': self.user.username,
	# 		'reply_on_comment': comment.id
	# 		})
	# 	response_content = str(response.content, encoding='utf8')
	# 	self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )




class FetchReplyPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.comment = PostComments.objects.create(comment_desc="Test Comment", post=cls.post, com_user=cls.user)
		cls.reply = PostComments.objects.create(comment_desc="Test Reply", post=cls.post, com_user=cls.user, com_reply=cls.user, reply_on_comment=cls.comment.id)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test fetch reply view with get request when not logged in
	def test_fetch_reply_view_get_nl(self):
		response = self.client.get(reverse("post:fr", kwargs={'id': self.comment.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test fetch reply with get request when not logged in and follow redirect
	def test_fetch_reply_view_get_nl_fr(self):
		response = self.client.get(reverse("post:fr", kwargs={'id': self.comment.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test fetch reply view with get request when logged in
	def test_fetch_reply_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:fr", kwargs={'id': self.comment.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# print(response_content)
		# self.assertContains(response, "deleted")
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )


	# test fetch reply with post request when logged in and follow redirect
	def test_fetch_reply_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.post(reverse("post:fr", kwargs={'id': self.comment.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "object"}'
		# )

		
	# test fetch reply with post request for reply on reply
	def test_fetch_reply_view_post_for_reply_on_reply(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		reply2 = PostComments.objects.create(comment_desc="Test Reply on Reply", post=self.post, com_user=self.user, com_reply=self.user, reply_on_comment=self.reply.id)
		response = self.client.get(reverse("post:fr", kwargs={'id': self.comment.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )




class EditCommentPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.comment = PostComments.objects.create(comment_desc="Test Comment", post=cls.post, com_user=cls.user)
		cls.reply = PostComments.objects.create(comment_desc="Test Reply", post=cls.post, com_user=cls.user, com_reply=cls.user, reply_on_comment=cls.comment.id)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test edit comment view with get request when not logged in
	def test_edit_comment_view_get_nl(self):
		response = self.client.get(reverse("post:ec", kwargs={'id': self.comment.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test edit comment view with get request when not logged in and follow redirect
	def test_edit_comment_view_get_nl_fr(self):
		response = self.client.get(reverse("post:ec", kwargs={'id': self.comment.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test edit comment view with get request when logged in
	def test_edit_comment_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:ec", kwargs={'id': self.comment.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertContains(response, "deleted")
		self.assertJSONEqual( 
			response_content,
			'{"result": "Error"}'
		)


	# test edit comment with post request when logged in and follow redirect
	def test_edit_comment_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")


		response = self.client.post(reverse("post:ec", kwargs={'id': self.comment.id}), {
			'comment_desc': 'test edit comment'
			})
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "object"}'
		# )

		

	# test edit comment with post request when logged in and invalid form
	def test_edit_comment_view_post_invalid_form(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.get(reverse("post:ec", kwargs={'id': self.comment.id}), {
			'comment_desc': ''
			})
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual( 
			response_content,
			'{"result": "Error"}'
		)

	# test edit reply with post request when logged in
	def test_edit_reply_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		# print(comment)
		response = self.client.post(reverse("post:ec", kwargs={'id': self.reply.id}), {
			'comment_desc': 'Test Edit Reply'
			})
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertJSONEqual( 
		# 	response_content,
		# 	'{"result": "error"}'
		# )




class DeleteCommentPostTest(TestCase):
		
	@classmethod
	def setUpTestData(cls):
		# super(PostTest, cls).setUpClass()
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.comment = PostComments.objects.create(comment_desc="Test Comment", post=cls.post, com_user=cls.user)
		cls.reply = PostComments.objects.create(comment_desc="Test Reply", post=cls.post, com_user=cls.user, com_reply=cls.user, reply_on_comment=cls.comment.id)
		cls.credentials = {
			'username': 'shah@gmail.com',
			'password': '@@123456'
		}


	def setUp(self):
		pass


	# test delete comment view with get request when not logged in
	def test_delete_comment_view_get_nl(self):
		response = self.client.get(reverse("post:dc", kwargs={'id': self.comment.id}))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "post/detpost.html")
		# self.assertContains(response, "<h1>You are not Logged In !!!</h1>")

	# test delete comment view with get request when not logged in and follow redirect
	def test_delete_comment_view_get_nl_fr(self):
		response = self.client.get(reverse("post:dc", kwargs={'id': self.comment.id}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")



	# test delete comment view with get request when logged in
	def test_delete_comment_view_get(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		response = self.client.get(reverse("post:dc", kwargs={'id': self.comment.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		# self.assertContains(response, "deleted")
		self.assertJSONEqual( 
			response_content,
			'{"result": "Error"}'
		)


	# test delete comment with post request when logged in and follow redirect
	def test_delete_comment_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.post(reverse("post:dc", kwargs={'id': self.comment.id}))
		response_content = str(response.content, encoding='utf8')
		# print(response_content)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual( 
			response_content,
			'{"result": "{\\"result\\": \\"Deleted\\", \\"id\\": \\"'+str(self.comment.id)+'\\"}"}'
		)

		

	# test delete comment with post request when logged in and invalid form
	def test_delete_comment_view_post_invalid_form(self):
		self.client.login(username=self.credentials['username'], password="@@123456")

		response = self.client.post(reverse("post:dc", kwargs={'id': 100000}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual( 
			response_content,
			'{"result": "Comment Does Not Exist"}'
		)

	# test delete reply with post request when logged in
	def test_delete_reply_post_view_post(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		# print(comment)
		response = self.client.post(reverse("post:dc", kwargs={'id': self.reply.id}))
		response_content = str(response.content, encoding='utf8')
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual( 
			response_content,
			'{"result": "{\\"result\\": \\"Deleted\\", \\"id\\": \\"'+str(self.reply.id)+'\\"}"}'
		)


