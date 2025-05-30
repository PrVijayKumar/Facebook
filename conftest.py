import pytest
from django.contrib.auth import get_user_model
from post.models import PostModel, PostLikes, PostComments
CustomUser = get_user_model()
from pytest_factoryboy import register
from post.tests.factories import CustomUserFactory, PostModelFactory, PostCommentsFactory, PostLikesFactory
from faker import Faker
fake = Faker()

# register factory
register(CustomUserFactory)
register(PostModelFactory)
register(PostCommentsFactory)
register(PostLikesFactory)



@pytest.fixture()
def post_api_fix(db, custom_user_factory, post_model_factory):
	user_data = {
            'username': fake.first_name(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': 'Test@12345',
            're_password': 'Test@12345',
            'contact': '1234569870'
        }
	# user.username= "TestUser"
	# user.set_password("@@123456")
	# post_data = {
	# 	'post_title': fake.name(),
	# 	'post_user': user,
	# 	'post_description': fake.text()
	# }
	return user_data


# using PostModelFactory to create fixtures
@pytest.fixture
def new_cpost(db, post_model_factory):
	post = post_model_factory.build()
	return post


# using PostCommentsFactory to create fixtures
@pytest.fixture
def new_ccomment(db, post_comments_factory):
	comment = post_comments_factory.build()
	return comment


# using PostLikesPost to create fixtures
@pytest.fixture
def new_clike(db, post_likes_factory):
	like = post_likes_factory.build()
	return like

# using CustomUserFactory to create fixtures
@pytest.fixture
def new_cuser1(db, custom_user_factory):
	user = custom_user_factory.create()
	# user = custom_user_factory.build()
	return user



@pytest.fixture()
def user1(db):
	user = CustomUser.objects.create_user(username="Shahrukh",
			first_name="Shahrukh",
			last_name="Khan",
			email="shah@gmail.com",
			contact="1234567890",
			dob="2000-04-29")
	return user



# creating a user factory for test User Model
@pytest.fixture
def new_user_factory():
	def create_app_user(
			username: str,
			password: str = None,
			first_name: str = "firstname",
			last_name: str = "lastname",
			email: str = "test@gmail.com",
			is_staff: str = False,
			is_superuser: str = False,
			is_active: str = True,
	):
		user = CustomUser.objects.create_user(
			username=username,
			password=password,
			first_name=first_name,
			last_name=last_name,
			email=email,
			is_staff=is_staff,
			is_superuser=is_superuser,
			is_active=is_active
		)
		return user
	return create_app_user


#  using above factory function fixture in a new fixture
@pytest.fixture
def new_user1(db, new_user_factory):
	return new_user_factory("Test_user", "password", "MyName")


# using above factory function fixture in a new fixture
@pytest.fixture
def new_user2(db, new_user_factory):
	return new_user_factory("Test_user", "password", "MyName", is_staff=True)


# fixture for postmodel
@pytest.fixture
def new_post(db, user1):
	user = user1
	post = PostModel.objects.create(
			post_title="Test Post",
			post_user=user,
			post_description="This post is created for testing purpose.",
			post_content="images/yellowcar.webp"
		)
	
	return user1, post



# fixture for post comments
@pytest.fixture
def postcom(db, new_post):
	user1, post = new_post
	comment = PostComments.objects.create(
				comment_desc="Test Comment",
				post=post,
				com_user=user1
			)
	reply = PostComments.objects.create(
				comment_desc="Test Reply",
				post=post,
				com_user=user1,
				com_reply=user1,
				reply_on_comment=comment.id
			)
	
	return comment, reply, user1, post



# fixture for testing postlikes
@pytest.fixture
def postlike(db, new_post):
	user1, post = new_post
	like = PostLikes.objects.create(post_id=post, liked_by=user1)
	return user1, post, like


	







# creating a factory
# @pytest.fixture()
# def new_user_factory(db):
# 	def create_app_user(
# 		username: str,
# 		password: str = None,
# 		first_name: str = "firstname",
# 		last_name: str = "lastname",
# 		email: str = "test@test.com",
# 		is_staff: str = False,
# 		is_superuser: str = False,
# 		is_active: str = True,
# 		contact: str = "1234567890",
# 		dob: str = "2000-04-29"
# 	):
# 		user = CustomUser.objects.create_user(
# 			username=username,
# 			password=password,
# 			first_name=first_name,
# 			last_name=last_name,
# 			email=email,
# 			is_staff=is_staff,
# 			is_superuser=is_superuser,
# 			is_active=is_active,
# 			contact=contact,
# 			dob=dob
# 		)
# 		return user
# 	return create_app_user



# @pytest.fixture
# def new_user(db, new_user_factory):
# 	return new_user_factory("Test_User", "password", "MyName")