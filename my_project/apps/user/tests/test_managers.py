from django.test import TestCase
from django.contrib.auth import get_user_model
CustomUser = get_user_model()


class TestUserCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_superuser_creation(self):
        # user = CustomUser.create_superuser()
        user = CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)

    def test_superuser_creation_is_staff_false(self):
        # user = CustomUser.create_superuser()
        # user = CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
		# 	dob="2000-04-29", is_staff=False)
        with self.assertRaisesRegex(ValueError, "Superuser must have is_staff=True."):
            CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29", is_staff=False)
        # self.assertIsNotNone(user)
        # self.assertTrue(user.is_superuser)


    def test_superuser_creation_is_superuser_false(self):
        # user = CustomUser.create_superuser()
        # user = CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
		# 	dob="2000-04-29", is_staff=False)
        with self.assertRaisesRegex(ValueError, "Superuser must have is_superuser=True."):
            CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29", is_superuser=False)
        # self.assertIsNotNone(user)
        # self.assertTrue(user.is_superuser)

    def test_user_creation(self):
        # user = CustomUser.create_superuser()
        user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
        self.assertIsNotNone(user)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)