import pytest
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

@pytest.mark.django_db
def test_user_create():
	CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29")
	count = CustomUser.objects.all().count()
	print(count)
	assert CustomUser.objects.count() == 1


@pytest.mark.django_db
def test_user_create1():
	count = CustomUser.objects.all().count()
	print(count)
	assert count == 0