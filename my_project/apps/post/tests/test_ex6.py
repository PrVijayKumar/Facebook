import pytest
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# using the factory of CustomUserFactory 
# we use small letter and _  when using factory
# use CustomUserFactory as custom_user_factory
# def test_new_user(custom_user_factory):
#     print(custom_user_factory.username)
#     assert True


# using cutom_user_factory.build() method to create an object
# def test_new_user(db, custom_user_factory):

# @pytest.mark.django_db
# def test_new_user(custom_user_factory):
#     # user = custom_user_factory.build()
#     user = custom_user_factory.create()
#     count = CustomUser.objects.all().count()
#     print(count)
#     print(user.username)
#     assert True




# using new_cuser1 fixture for test\
# def test_new_user(new_cuser1):
#     print(new_cuser1.username)
#     assert True


# using postmodel_factory 
# def test_new_post(post_model_factory):
#     post = post_model_factory.build()
#     print(post.post_description)
#     assert True


# using postmodel_factory 
def test_new_post(db, post_model_factory):
    post = post_model_factory.create()
    print(post.post_description)
    # print(post.post_user)
    assert True



