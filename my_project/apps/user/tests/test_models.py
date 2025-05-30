from django.test import TestCase
from user.models import CustomUser
from django.utils import timezone



# Create your tests here.
class CustomUserModelTest(TestCase):

	# fixtures = ["mydata.json"]

	# classmethod setUpTestData to set up data all the test cases
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")

	# setUp function provides separate data for each test run
	# for initialization 
	def setUp(self):
		pass


	# tearDown function for tests
	# for clean up work
	def tearDown(self):
		CustomUser.objects.all().delete()


	# test for model creation
	def test_model_creation(self):
		user = CustomUser.objects.get(id=self.user.id)
		user2 = CustomUser.objects.filter(email="bajaj@gmail.com")
		print(user2)
		self.assertIsNotNone(user)

	# test to check all the values are correctly stored
	def test_first_name_label(self):
		user = CustomUser.objects.get(id=self.user.id)
		field_label = user._meta.get_field('first_name').verbose_name
		self.assertEqual(field_label, 'first name')

	# test to check the label of last name
	def test_last_name_label(self):
		user = CustomUser.objects.get(id=self.user.id)
		field_label = user._meta.get_field('last_name').verbose_name
		self.assertEqual(field_label, 'last name')


	# test to check the label of email
	# def test_email_label(self):
	# 	user = CustomUser.objects.get(id=1)
	# 	field_label = user._meta.get_field('email').verbose_name
	# 	self.assertEqual(field_label, 'email')

	# test to check the max length of username
	def test_username_max_length(self):
		user = CustomUser.objects.get(id=self.user.id)
		max_length = user._meta.get_field('username').max_length
		self.assertEqual(max_length, 32)


	# test to check the max length of first name
	def test_first_name_max_length(self):
		user = CustomUser.objects.get(id=self.user.id)
		max_length = user._meta.get_field('first_name').max_length
		self.assertEqual(max_length, 150)


	# test to check the max length of last name
	def test_last_name_max_length(self):
		user = CustomUser.objects.get(id=self.user.id)
		max_length = user._meta.get_field('last_name').max_length
		self.assertEqual(max_length, 150)

	# test to check the str value of user
	def test_object_name_email(self):
		user = CustomUser.objects.get(id=self.user.id)
		expected_object_name = f'{user.email}'
		assert str(user) == expected_object_name
		# self.assertEqual(str(user), expected_object_name)


	# test to get absolute url
	def test_get_absolute_url(self):
		user = CustomUser.objects.get(id=self.user.id)
		self.assertEqual(user.get_absolute_url(), f'/user/{user.id}/')


	# test to check the label of is superuser
	def test_is_superuser_label(self):
		user = CustomUser.objects.get(id=self.user.id)
		field_label = user._meta.get_field('is_superuser').verbose_name
		self.assertEqual(field_label, 'superuser status')


	# test to check the label of is staff
	def test_is_staff_label(self):
		user = CustomUser.objects.get(id=self.user.id)
		field_label = user._meta.get_field('is_staff').verbose_name
		self.assertEqual(field_label, 'staff status')


	# test to check the label of is active
	def test_is_active_label(self):
		user = CustomUser.objects.get(id=self.user.id)
		field_label = user._meta.get_field('is_active').verbose_name
		self.assertEqual(field_label, 'active')


	# test to check to date joined
	def test_date_joined_label(self):
		user = CustomUser.objects.get(id=self.user.id)
		field_label = user._meta.get_field('date_joined').verbose_name
		self.assertEqual(field_label, 'date joined')


	# test to check if the correct values are inserted in the CustomUser DB
	def test_data_included_in_db(self):
		user = CustomUser.objects.get(id=self.user.id)
		self.assertEqual(user.username, "Shahrukh")
		self.assertEqual(user.first_name, "Shahrukh")
		self.assertEqual(user.last_name, "Khan")
		self.assertEqual(user.email, "shah@gmail.com")
		self.assertEqual(user.contact, "1234567890")
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_superuser)
		self.assertFalse(user.is_staff)
		self.assertEqual(user.date_joined.date(), timezone.now().date())
		self.assertEqual(user.password, "@@123456")
		self.assertEqual(str(user.dob), "2000-04-29")







	# test to check the value returned by str

		# CustomUser.objects.create(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890")
