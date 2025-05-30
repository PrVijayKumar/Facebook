import pytest


# fixture 
# @pytest.fixture()
# def user1():
# 	return CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", dob="2000-04-29")


# # set the password and access db
# @pytest.mark.django_db
# def test_set_check_password(user1):
# 	user1.set_password('new-password')
# 	assert user1.check_password('new-password') is True


# fixture



# seththe password and access db
# @pytest.mark.django_db
# def test_set_check_password(user1):
# 	assert user1.username == "Shahrukh"


# @pytest.mark.django_db
# def test_set_check_password1(user1):
# 	print('check user 1')
# 	assert user1.username == "Shahrukh"


# @pytest.mark.django_db
# def test_set_check_password2(user1):
# 	print('check user 2')
# 	assert user1.username == "Shahrukh"


@pytest.mark.django_db
def test_set_check_password2(new_user):
	print(new_user.first_name)
	assert new_user.first_name == "MyName"