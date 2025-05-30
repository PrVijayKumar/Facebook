import factory
from faker import Faker
from django.contrib.auth import get_user_model
from post.models import PostModel, PostLikes, PostComments
CustomUser = get_user_model()
fake = Faker()


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = fake.name()
    is_staff = "True"


class PostModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostModel

    post_title = "Django Post"
    post_user = factory.SubFactory(CustomUserFactory)
    post_description = fake.text()
    post_content = "images/yellowcar.webp"


class PostCommentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostComments

    comment_desc = fake.text()
    post = factory.SubFactory(PostModelFactory)
    com_user = factory.SubFactory(CustomUserFactory)


    


class PostLikesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostLikes

    post_id = factory.SubFactory(PostModelFactory)
    liked_by = factory.SubFactory(CustomUserFactory)

