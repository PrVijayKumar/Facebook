from django.test import TestCase
from post.models import PostModel, PostComments, PostLikes
from user.models import CustomUser
from django.utils import timezone




class PostModelTest(TestCase):

	# setUpClass function not working above django 1.8
	# use setUpTestData
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")


	# setUp function
	def setUp(self):
		pass


	# test to check the post title
	def test_model_creation(self):
		self.assertIsNotNone(self.post)

	# test post title
	def test_post_data(self):
		self.assertEqual(self.post.post_title, "Test Post")
		# self.assertEqual(self.post.post_user, "shah@gmail.com")
		self.assertEqual(self.post.post_user.id, self.user.id)
		self.assertEqual(self.post.post_description, "This post is created for testing purpose.")
		self.assertEqual(self.post.post_content, "images/yellowcar.webp")
		self.assertEqual(str(self.post.post_date.date()), str(timezone.now().date()))
		self.assertEqual(self.post.post_likes, 0)



	# test post title max length
	def test_post_title_max_length(self):
		max_length = self.post._meta.get_field('post_title').max_length
		self.assertEqual(max_length, 200)


	# test post description max length
	def test_post_desc_max_length(self):
		max_length = self.post._meta.get_field('post_description').max_length
		self.assertEqual(max_length, None)

	# test post likes 
	def test_post_likes(self):
		likes = self.post.post_likes
		self.assertEqual(likes, 0)



	# test 




# Testing Comments Model
class PostCommentTest(TestCase):

	# setUpTestData function
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.comment = PostComments.objects.create(comment_desc="Test Comment", post=cls.post, com_user=cls.user)
		cls.reply = PostComments.objects.create(comment_desc="Test Reply", post=cls.post, com_user=cls.user, com_reply=cls.user,
			reply_on_comment=cls.comment.id)


	# test the model creation
	def test_model_creation(self):
		self.assertIsNotNone(self.comment)
		self.assertIsNotNone(self.reply)


	# test the comment data
	def test_post_comment_data(self):
		self.assertEqual(self.comment.comment_desc, "Test Comment")
		self.assertEqual(self.comment.com_user_id, self.user.id)
		self.assertEqual(str(self.comment.com_date.date()),str(timezone.now().date()))
		self.assertEqual(self.comment.com_reply_id, None)
		self.assertEqual(self.comment.com_likes, 0)
		self.assertEqual(self.comment.reply_on_comment, None)
		self.assertEqual(str(self.comment.updated_at.date()), str(timezone.now().date()))

	# # test the reply data
	def test_comment_reply_data(self):
		self.assertEqual(self.reply.comment_desc, "Test Reply")
		self.assertEqual(self.reply.com_user_id, self.user.id)
		self.assertEqual(str(self.reply.com_date.date()), str(timezone.now().date()))
		self.assertEqual(self.reply.com_reply_id, self.comment.com_user_id)
		self.assertEqual(self.reply.reply_on_comment, self.comment.id)
		self.assertEqual(str(self.reply.updated_at.date()), str(timezone.now().date()))


	# test to check the max length of comment and reply
	def test_comment_reply_max_length(self):
		com_max_length = self.comment._meta.get_field('comment_desc').max_length
		rep_max_length = self.reply._meta.get_field('comment_desc').max_length
		self.assertEqual(com_max_length, 200)
		self.assertEqual(rep_max_length, 200)


	# test to check the label of fields
	def test_comment_fields_labels(self):
		com_desc_label = self.comment._meta.get_field('comment_desc').verbose_name
		com_user_label = self.comment._meta.get_field('com_user').verbose_name
		com_date_label = self.comment._meta.get_field('com_date').verbose_name
		com_reply_label = self.comment._meta.get_field('com_reply').verbose_name
		com_likes_label = self.comment._meta.get_field('com_likes').verbose_name
		reply_on_comment_label = self.comment._meta.get_field('reply_on_comment').verbose_name
		updated_at_label = self.comment._meta.get_field('updated_at').verbose_name
		self.assertEqual(com_desc_label, 'comment desc')
		self.assertEqual(com_user_label, 'com user')
		self.assertEqual(com_date_label, 'com date')
		self.assertEqual(com_reply_label, 'com reply')
		self.assertEqual(com_likes_label, 'com likes')
		self.assertEqual(reply_on_comment_label, 'reply on comment')
		self.assertEqual(updated_at_label, 'updated at')



# Testing Likes Model
class PostLikesTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
		cls.post = PostModel.objects.create(post_title="Test Post", post_user=cls.user, post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp")
		cls.like = PostLikes.objects.create(post_id=cls.post, liked_by=cls.user)


	# set Up Function
	def setUp(self):
		pass


	# test the model creation
	def test_model_creation(self):
		self.assertIsNotNone(self.like)


	# test to check the likes data
	def test_post_likes_data(self):
		self.assertEqual(self.like.post_id_id, self.post.id)
		self.assertEqual(self.like.liked_by_id, self.user.id)
		self.assertEqual(str(self.like.created_at.date()), str(timezone.now().date()))
		self.assertEqual(str(self.like.updated_at.date()), str(timezone.now().date()))


	# test to check the label
	def test_post_likes_field_label(self):
		post_id_label = self.like._meta.get_field('post_id').verbose_name
		liked_by_label = self.like._meta.get_field('liked_by').verbose_name
		created_at_label = self.like._meta.get_field('created_at').verbose_name
		updated_at_label = self.like._meta.get_field('updated_at').verbose_name
		self.assertEqual(post_id_label, "post id")
		self.assertEqual(liked_by_label, "liked by")
		self.assertEqual(created_at_label, "created at")
		self.assertEqual(updated_at_label, "updated at")