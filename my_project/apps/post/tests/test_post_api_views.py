from rest_framework.test import APITestCase, APIClient
import pytest
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from faker import Faker
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
import pathlib
from django.core.files.uploadedfile import SimpleUploadedFile
# from PIL import Image
import json
from post.models import PostComments, PostModel, PostLikes
# import base64
# from io import BytesIO
fake = Faker()
# @pytest.mark.usefixtures("post_api_fix")
class TestPostAPIViews(APITestCase):

    @pytest.fixture(autouse=True)
    def api_data_set_up(self, post_api_fix):
        self.client = APIClient()
        self.user_data = post_api_fix
        self.client.post(reverse('create_apiuser'), self.user_data, format="json")
        self.user = CustomUser.objects.get(username=self.user_data['username'])
        self.post_data = {
                    'post_title': fake.name(),
                    # 'post_user_id': self.user.id,
                    'post_description': fake.text()
	                }
    @classmethod 
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.user_data = {
            'username': fake.first_name(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password': 'Test@12345',
            're_password': 'Test@12345',
            'contact': '1234569870'
        }
        cls.client.post(reverse('create_apiuser'), cls.user_data, format="json")
        cls.user = CustomUser.objects.get(username=cls.user_data['username'])
        cls.post_data = {
                    'post_title': fake.name(),
                    # 'post_user_id': self.user.id,
                    'post_description': fake.text()
	                }


    def test_post_creation(self):
        self.client.login(username=self.user.username, password="Test@12345")
        path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
        myimg = open(path, 'rb')
        f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")
        # with open(path, "rb") as myimg:
        #     image_data = base64.b64encode(myimg.read()).decode('utf-8')
        self.post_data['post_content'] = f

        response = self.client.post(reverse("post-list"), self.post_data, format="multipart")
        assert response.status_code == 201


    def test_getting_post_list(self):
        self.client.login(username=self.user.username, password="Test@12345")
        path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
        myimg = open(path, 'rb')
        f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")
        # with open(path, "rb") as myimg:
        #     image_data = base64.b64encode(myimg.read()).decode('utf-8')
        self.post_data['post_content'] = f

        self.client.post(reverse("post-list"), self.post_data, format="multipart")
        response = self.client.get(reverse("post-list"), format="json")
        assert response.status_code == 200

    def test_getting_post_list_by_superuser(self):
        suser = CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29", is_staff=True, is_superuser=True)
        self.client.login(username=suser.username, password="@@123456")
        path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
        myimg = open(path, 'rb')
        f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")
        # with open(path, "rb") as myimg:
        #     image_data = base64.b64encode(myimg.read()).decode('utf-8')
        self.post_data['post_content'] = f

        self.client.post(reverse("post-list"), self.post_data, format="multipart")
        response = self.client.get(reverse("post-list"), format="json")
        assert response.status_code == 200


    def test_getting_particular_post(self):
        self.client.login(username=self.user.username, password="Test@12345")
        path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
        myimg = open(path, 'rb')
        f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")
        # with open(path, "rb") as myimg:
        #     image_data = base64.b64encode(myimg.read()).decode('utf-8')
        self.post_data['post_content'] = f

        res = self.client.post(reverse("post-list"), self.post_data, format="multipart")
        res_content = json.loads(res.content)
        print(res_content['id'])
        response = self.client.get(reverse("post-detail", kwargs={'pk': res_content['id']}), format="json")
        assert response.status_code == 200

    def test_getting_particular_post_by_superuser(self):
        suser = CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29", is_staff=True, is_superuser=True)
        self.client.login(username=suser.username, password="@@123456")
        path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
        myimg = open(path, 'rb')
        f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")
        # with open(path, "rb") as myimg:
        #     image_data = base64.b64encode(myimg.read()).decode('utf-8')
        self.post_data['post_content'] = f

        res = self.client.post(reverse("post-list"), self.post_data, format="multipart")
        res_content = json.loads(res.content)
        print(res_content['id'])
        response = self.client.get(reverse("post-detail", kwargs={'pk': res_content['id']}), format="json")
        # response = self.client.get(reverse("post-list"), format="json")

        assert response.status_code == 200

    def test_updating_particular_post(self):
        self.client.login(username=self.user.username, password="Test@12345")
        path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
        myimg = open(path, 'rb')
        f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")
        # with open(path, "rb") as myimg:
        #     image_data = base64.b64encode(myimg.read()).decode('utf-8')
        self.post_data['post_content'] = f

        res = self.client.post(reverse("post-list"), self.post_data, format="multipart")
        res_content = json.loads(res.content)
        print(res_content['id'])

        # modify data
        self.post_data = {
            'post_title': 'updated title',
            'post_description': 'updated description',
        }
        up_post = PostModel.objects.get(id=res_content['id'])
        breakpoint()
        response = self.factory.patch(reverse("post-detail", kwargs={'pk': res_content['id']}), data = json.dumps(self.post_data), content_type="application/json")
        
        print(PostModel.objects.count())
        up_post.refresh_from_db()
        # print("checking response", response.__dict__)
        self.assertEqual(up_post.post_title,'updated title')
        # assert response.REQUEST_METHOD == 'PUT'


    def test_updating_particular_post_by_superuser(self):
        suser = CustomUser.objects.create_superuser(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
			dob="2000-04-29", is_staff=True, is_superuser=True)
        self.client.login(username=suser.username, password="@@123456")
        path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()/'media/images'/'yellowcar.webp'
        myimg = open(path, 'rb')
        f = SimpleUploadedFile("birthday.jpeg", myimg.read(), content_type="images/webp")
        # with open(path, "rb") as myimg:
        #     image_data = base64.b64encode(myimg.read()).decode('utf-8')
        self.post_data['post_content'] = f

        res = self.client.post(reverse("post-list"), self.post_data, format="multipart")
        res_content = json.loads(res.content)
        print(res_content['id'])

        # modify data
        self.post_data = {
            'post_title': 'updated title',
            'post_description': 'updated description'
        }

        response = self.client.patch(reverse("post-detail", kwargs={'pk': res_content['id']}), self.post_data, content_type="application/json")
        # response = self.client.get(reverse("post-list"), format="json")
        print(response)
        assert response.status_code == 201
    
        # files = {'post_content': f}
        # print(image_data)
        # breakpoint()
        # img = Image.open(path)
        # buffered = BytesIO()
        # img.save(buffered, format="WEBP")
        # img_byte = buffered.getvalue()
        # img_base64 = base64.b64encode(img_byte)
        # img_str = img_base64.decode('utf-8')
        # files = {
        #     'text': 'image',
        #     'img': img_str
        # }
        # self.post_data['post_content'] = files['img']
        # print(self.post_data.keys())
        # data = json.dumps(self.post_data)
        # print(data)
        # data = json.loads(data)
        # response = self.client.login(username=self.user.username, password="@@123456")
        # # response = self.client.post(self.register_url)
        # print(response)
        # self.assertEqual(response.status_code, 400)


    
    # def test_user_can_register_correctly(self):
    #     response = self.client.post(
    #         self.register_url, self.user_data, format="json")
    #     self.assertEqual(response.data['user']['email'], self.user_data['email'])
    #     self.assertEqual(response.data['user']['username'], self.user_data['username'])
    #     self.assertEqual(response.status_code, 201) # it should be 201

    # def test_user_can_register_without_last_name_correctly(self):
    #     self.user_data.pop('last_name')
    #     response = self.client.post(
    #         self.register_url, self.user_data, format="json")
    #     self.assertEqual(response.data['user']['email'], self.user_data['email'])
    #     self.assertEqual(response.data['user']['username'], self.user_data['username'])
    #     self.assertEqual(response.status_code, 201) # it should be 201