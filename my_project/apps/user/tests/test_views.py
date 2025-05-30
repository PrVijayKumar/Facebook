from django.test import TestCase
from post.models import PostModel, PostComments, PostLikes
from user.models import CustomUser, Codes
from django.utils import timezone
from django.urls import reverse
from user.tasks import reset_pass_email
from unittest.mock import patch
class AllPostsTest(TestCase):

	@classmethod
	def setUpClass(cls):
		super(AllPostsTest, cls).setUpClass()
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
		self.assertTemplateUsed(response, 'user/allposts.html')




	# test template content
	def test_template_content_when_not_logged_in(self):

		response = self.client.get(reverse('user:apost'))
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")
		response = self.client.post(reverse('user:apost'),
			{
				'username':self.credentials['username'],
				'password': '@@123456',
			}
			)
		self.assertContains(response, "<h1>You are not Logged In !!!</h1>")


	# test template content
	def test_template_content_when_logged_in(self):
		self.client.login(username=self.credentials['username'], password="@@123456")
		response = self.client.get(reverse('user:apost'))
		self.assertContains(response, f"<h1>Hello, {self.user.username}</h1>")

		response = self.client.post(reverse('user:apost'))
		self.assertContains(response, f"<h1>Hello, {self.user.username}</h1>")



class ForgotPasswordTests(TestCase):

	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")


	# test url exists 



	# test the fpassword view function redirect
	def test_fpassword_view_function_redirect(self):
		response = self.client.post(reverse('user:forgotpass'), {'email': self.user.email})
		self.assertEqual(response.status_code, 302)


	# test the fpassword view return errormsg if email doesn't exist
	def test_fpassword_view_function_returns_error(self):
		response = self.client.post(reverse('user:forgotpass'), {'email': 'unknown@gmail.com'})
		self.assertContains(response, 'No search results')


	"""test the fpassword returns a correct template with correct email"""
	def test_fpassword_view_function_returns_correct_template_with_email(self):
		response = self.client.post(reverse('user:forgotpass'), {'email': self.user.email}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/rpass.html")
		self.assertContains(response, "Reset Your Password")


class ResetPasswordTests(TestCase):

	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")


	# test the rpassword view function
	def test_rpassword_view_function_with_post_request(self):
		response = self.client.post(reverse('user:respass', kwargs={'id': self.user.id}), {'email': self.user.email})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/rpass.html')
		self.assertContains(response, "Reset Your Password")


# test the reset code confirmation view
class RCodeTests(TestCase):

	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")


	# test the rcode view function
	def test_rcode_view_function_with_post_request_fb(self):
		# test for facebook notification opt 1
		response = self.client.post(reverse('user:rcode', kwargs={'id': self.user.id}), {'ropt': 1})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/rcode.html")
		self.assertContains(response, "We sent a 6-digit code to another device")

	# test the rcode view function sms
	def test_rcode_view_function_with_post_request_sms(self):
		# test for Code via SMS opt 2
		response = self.client.post(reverse('user:rcode', kwargs={'id': self.user.id}), {'ropt': 2})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/ecode.html")
		self.assertContains(response, "Please check your phone for an email message with your code.")


	# test the rcode view function email
	# @patch('user.tasks.reset_pass_email')
	def test_rcode_view_function_with_post_request_email(self):
		# test for Code via Email opt 3
		response = self.client.post(reverse('user:rcode', kwargs={'id': self.user.id}), {'ropt': 3})
		# mock_reset_pass_email.assert_called_once_with(self.user.username, self.user.email, self.user.id)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, "Log In")


	# test the rcode view function other option
	def test_rcode_view_function_with_post_request_op(self):
		# test for Code with other option
		response = self.client.post(reverse('user:rcode', kwargs={'id': self.user.id}), {'ropt': 5})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/rpass.html")
		self.assertContains(response, "Reset Your Password")


	# test the rcode view function with get request
	def test_rcode_view_function_with_get_request(self):
		response = self.client.get(reverse('user:rcode', kwargs={'id': self.user.id}))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/rpass.html")
		self.assertContains(response, "Reset Your Password")


# test vcode view 
class VCodeTests(TestCase):

	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")

	# test the vcode view function
	# @patch('user.tasks.reset_pass_email')
	def test_vcode_view_function_with_post_request_code_exists(self):
		# test for facebook notification opt 1
		code = Codes.objects.create(source='E', user_id=self.user.id, code='12345678')
		response = self.client.post(reverse('user:vcode', kwargs={'id': self.user.id}), {'rcode': code.code})
		# mock_reset_pass_email.assert_called_once_with(self.user.username, self.user.email, self.user.id)
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "user/rcode.html")
		# self.assertContains(response, "We sent a 6-digit code to another device")

	# test the vcode view function follow redirect
	def test_vcode_view_function_with_post_request_redirect_code_exists(self):
		code = Codes.objects.create(source='E', user_id=self.user.id, code='12345678')
		response = self.client.post(reverse('user:vcode', kwargs={'id': self.user.id}), {'rcode': code.code}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/respass.html")
		self.assertContains(response, "Create a new password that is atleast 6 characters long.")



	# test the vcode view function when code does not exist
	def test_vcode_view_function_with_post_request_code_not_exists(self):
		response = self.client.post(reverse('user:vcode', kwargs={'id': self.user.id}), {'rcode': 12345600}, HTTP_REFERER=reverse('user:rcode', kwargs={'id': self.user.id}))
		# mock_reset_pass_email.assert_called_once_with(self.user.username, self.user.email, self.user.id)
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "user/rcode.html")
		# self.assertContains(response, "We sent a 6-digit code to another device")

	# test the vcode view function when code does not exist and follow redirect
	def test_vcode_view_function_with_post_request_code_not_exists_follow_redirect(self):
		response = self.client.post(reverse('user:vcode', kwargs={'id': self.user.id}), {'rcode': 12345600}, HTTP_REFERER=reverse('user:rcode', kwargs={'id': self.user.id}), follow=True)
		# mock_reset_pass_email.assert_called_once_with(self.user.username, self.user.email, self.user.id)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/rpass.html")
		self.assertContains(response, "Reset Your Password")


	# test the vcode view function when code exists but wrong code entered
	def test_vcode_view_function_with_post_request_wrong_code_provided(self):
		code = Codes.objects.create(source='E', user_id=self.user.id, code='12345678')
		response = self.client.post(reverse('user:vcode', kwargs={'id': self.user.id}), {'rcode': 12345600}, HTTP_REFERER=reverse('user:rcode', kwargs={'id': self.user.id}), follow=True)
		# mock_reset_pass_email.assert_called_once_with(self.user.username, self.user.email, self.user.id)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/rpass.html")
		self.assertContains(response, "Reset Your Password")



	# tearDown for cleaning data
	def tearDown(self):
		Codes.objects.all().delete()



# test to check the reset password view
class ResetPasswordViewTest(TestCase):

	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")


	# test to check the response of resetpass view with get request
	def test_resetpass_get_request(self):
		response = self.client.get(reverse('user:resetpass', kwargs={'id': self.user.id}))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/respass.html")


	# test to check the response of resetpass view with post request when no data provided
	def test_resetpass_post_request(self):
		response = self.client.post(reverse('user:resetpass', kwargs={'id': self.user.id}))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/respass.html")

	# test to check the response of resetpass view with post request when data provided
	def test_resetpass_post_request_with_data(self):
		response = self.client.post(reverse('user:resetpass', kwargs={'id': self.user.id}), {'password': 'TestPass@@123'})
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, "user/respass.html")

	# test to check the response of resetpass view with post request when invalid password provided
	def test_resetpass_post_request_with_invalidpass(self):
		response = self.client.post(reverse('user:resetpass', kwargs={'id': self.user.id}), {'password': 'testpass1234'})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/respass.html")


	# test to check the response of resetpass view with post request when data provided follow redirect
	def test_resetpass_post_request_with_data_follow_redirect(self):
		response = self.client.post(reverse('user:resetpass', kwargs={'id': self.user.id}), {'password': 'TestPass@@123'}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, '<h1>Login with your new password</h1>')

	# test to check the response of resetpass view with post request when data provided follow redirect and code available
	def test_resetpass_post_request_with_data_follow_redirect(self):
		code = Codes.objects.create(source='E', user_id=self.user.id, code='12345678')
		response = self.client.post(reverse('user:resetpass', kwargs={'id': self.user.id}), {'password': 'TestPass@@123'}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "user/login.html")
		self.assertContains(response, '<h1>Login with your new password</h1>')




# test dashboard
class DashboardViewTest(TestCase):

	# set up test data
	# set up test data
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")


	# test get request for dashboard view
	def test_dashboard_with_get_request_not_logged_in(self):
		response = self.client.get(reverse('user:dashboard'))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, 'user/login.html')
		# self.assertContains(response, 'Log In')


	# test get request for dashboard view follow redirect
	def test_dashboard_with_get_request_not_logged_in_follow_redirect(self):
		response = self.client.get(reverse('user:dashboard'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/login.html')
		self.assertContains(response, 'Log In')


	# test post request for dashboard view 
	def test_dashboard_with_post_request_not_logged_in(self):
		response = self.client.post(reverse('user:dashboard'))
		self.assertEqual(response.status_code, 302)
		# self.assertTemplateUsed(response, 'user/login.html')
		# self.assertContains(response, 'Log In')



	# test post request for dashboard view follow redirect
	def test_dashboard_with_post_request_not_logged_in_follow_redirect(self):
		response = self.client.post(reverse('user:dashboard'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/login.html')
		self.assertContains(response, 'Log In')



	# test post request for dashboard view follow redirect
	def test_dashboard_with_post_request_logged_in_follow_redirect(self):
		self.client.login(username=self.user.username, password="@@123456")
		response = self.client.get(reverse('user:dashboard'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/allposts.html')
		self.assertContains(response, f'Hello, {self.user.username}')


	# test post request for dashboard view follow redirect and have posts and have likes
	def test_dashboard_with_post_request_not_logged_in_follow_redirect_posts_likes(self):
		post = PostModel.objects.create(post_title="Test Post", post_user=self.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		like = PostLikes.objects.create(post_id=post, liked_by=self.user)
		self.client.login(username=self.user.username, password="@@123456")
		response = self.client.post(reverse('user:dashboard'), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/allposts.html')
		self.assertContains(response, f'Hello, {self.user.username}')