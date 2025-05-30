import pytest
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


    
# @pytest.mark.django_db
# def test_check_set_password(user1):
#     user1.set_password("@@123456")
#     assert user1.check_password("@@123456") is True


# def test_username(user1):
#     assert user1.username == "Shahrukh"



# def test_new_user(new_user):
#     print(new_user.first_name)
#     assert new_user.first_name == "MyName"


# testing the new user 2 fixture for is_staff = True
def test_new_user(new_user2):
    print(new_user2.is_staff)
    assert new_user2.is_staff