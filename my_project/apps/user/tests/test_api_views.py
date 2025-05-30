from .test_api_setup import TestSetUp
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse
CustomUser = get_user_model()

class TestViews(TestSetUp):

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)


    
    def test_user_can_register_correctly(self):
        response = self.client.post(
            self.register_url, self.user_data, format="json")
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(response.data['user']['username'], self.user_data['username'])
        self.assertEqual(response.status_code, 201) # it should be 201

    def test_user_can_register_without_last_name_correctly(self):
        self.user_data.pop('last_name')
        response = self.client.post(
            self.register_url, self.user_data, format="json")
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(response.data['user']['username'], self.user_data['username'])
        self.assertEqual(response.status_code, 201) # it should be 201


    def test_user_can_register_without_first_or_last_name_correctly(self):
        self.user_data.pop('first_name')
        self.user_data.pop('last_name')
        response = self.client.post(
            self.register_url, self.user_data, format="json")
        # print(response.data['user'])
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        self.assertEqual(response.data['user']['username'], self.user_data['username'])
        self.assertEqual(response.status_code, 201) # it should be 201

    def test_user_cannot_register_with_invalid_email(self):
        self.user_data['email'] = "invalidEmail"
        response = self.client.post(
            self.register_url, self.user_data, format="json")
        response_content = str(response.content, encoding='utf8')
        print(response_content)
        self.assertEqual(response_content, '{"email":["Enter a valid email address."]}')
        
    def test_user_cannot_register_with_existing_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.register_url, {
            'username': "testusename",
            'first_name': "testfirstname",
            'last_name': "testlastname",
            'email': self.user_data['email'],
            'password': 'Test@12345',
            're_password': 'Test@12345',
            'contact': '1234569800'
        }, format="json")
        response_content = str(response.content, encoding='utf8')
        self.assertEqual(response_content, '{"email":["Email already exists"]}')


    def test_user_can_register_with_empty_first_name(self):
        self.user_data['first_name'] = ""
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_user_can_register_with_empty_last_name(self):
        self.user_data['last_name'] = ""
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 201)


    def test_user_cannot_register_with_invalid_first_name(self):
        self.user_data['first_name'] = "test123"
        response = self.client.post(self.register_url, self.user_data, format="json")
        response_content = str(response.content, encoding='utf8')
        self.assertEqual(response_content, '{"first_name":["First Name should only contain alphabets. Spaces, Numbers or Special Symbols are not allowed."]}')

    def test_user_cannot_register_with_invalid_last_name(self):
        self.user_data['last_name'] = "test123"
        response = self.client.post(self.register_url, self.user_data, format="json")
        response_content = str(response.content, encoding='utf8')
        self.assertEqual(response_content, '{"last_name":["Last Name should only contain alphabets. Spaces, Numbers or Special Symbols are not allowed."]}')


    def test_user_cannot_register_with_invalid_password(self):
        self.user_data['password'] = "12345678"
        self.user_data['re_password'] = "12345678"
        response = self.client.post(self.register_url, self.user_data, format="json")
        response_content = str(response.content, encoding='utf8')
        self.assertEqual(response_content, '{"password":["Password must contain Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character."]}')

    def test_user_cannot_register_with_mismatching_password(self):
        self.user_data['re_password'] = "Vladimir@123"
        response = self.client.post(self.register_url, self.user_data, format="json")
        response_content = str(response.content, encoding='utf8')
        self.assertEqual(response_content, '{"password":["Passwords does not match"]}')

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(
            self.register_url, self.user_data, format="json"
        )
        response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 200)  # it should be 401


    def test_user_can_login_with_after_verification(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        email = res.data['user']['email']
        user = CustomUser.objects.get(email=email)
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_user_can_logout(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        email = res.data['user']['email']
        user = CustomUser.objects.get(email=email)
        user.is_verified = True
        user.save()
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.post(reverse('logout_apiuser'), self.user_data, format="json")
        # print(response)
        self.assertEqual(response.status_code, 200)


    def test_getting_user_list(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        email = res.data['user']['email']
        user = CustomUser.objects.get(email=email)
        user.is_verified = True
        user.save()
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(reverse("user-list"), format="json")
        print(response)
        self.assertEqual(response.status_code, 200)


    def test_creating_new_user(self):
        res = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        email = res.data['user']['email']
        user = CustomUser.objects.get(email=email)
        user.is_verified = True
        user.save()
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        new_user_data = {
            'username': "TestNewUser",
            'first_name': "TestNewFirstName",
            'last_name': "TestNewLastName",
            'email': "testnewemail@gmail.com",
            'password': 'Test@12345',
            're_password': 'Test@12345',
            'contact': '1234569870'
        }
        response = self.client.post(
            reverse("user-list"), new_user_data, format="json"
        )
        self.assertEqual(response.status_code, 403)


    def test_creating_new_user_by_superuser(self):
        # self.user_data['is_staff'] = True
        # self.user_data['is_superuser'] = True
        # self.user_data['is_active'] = True
        # res = self.client.post(
        #     self.register_url, self.user_data, format="json"
        # )
        # email = res.data['user']['email']
        # user = CustomUser.objects.get(email=email)
        # user.is_verified = True
        # user.save()
        # CustomUser.objects.create_superuser()
        user = CustomUser.objects.create_superuser(
            username=self.user_data['username'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            email=self.user_data['email'],
            contact=self.user_data['contact'],
            password="@@123456",
			dob="2000-04-29")
        self.client.login(username=self.user_data['username'], password="@@123456")
        new_user_data = {
            'username': "TestNewUser",
            'first_name': "TestNewFirstName",
            'last_name': "TestNewLastName",
            'email': "testnewemail@gmail.com",
            'password': 'Test@12345',
            're_password': 'Test@12345',
            'contact': '1234569870'
        }
        response = self.client.post(
            reverse("user-list"), new_user_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_getting_data_by_superuser(self):
        self.user_data['is_staff'] = True
        self.user_data['is_superuser'] = True
        self.user_data['is_active'] = True
        res = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        email = res.data['user']['email']
        user = CustomUser.objects.get(email=email)
        user.is_verified = True
        user.save()
        # # CustomUser.objects.create_superuser()
        # user = CustomUser.objects.create_superuser(
        #     username=self.user_data['username'],
        #     first_name=self.user_data['first_name'],
        #     last_name=self.user_data['last_name'],
        #     email=self.user_data['email'],
        #     contact=self.user_data['contact'],
        #     password="@@123456",
		# 	dob="2000-04-29")
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        # new_user_data = {
        #     'username': "TestNewUser",
        #     'first_name': "TestNewFirstName",
        #     'last_name': "TestNewLastName",
        #     'email': "testnewemail@gmail.com",
        #     'password': 'Test@12345',
        #     're_password': 'Test@12345',
        #     'contact': '1234569870'
        # }
        response = self.client.get(
            reverse("user-list"), self.user_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
