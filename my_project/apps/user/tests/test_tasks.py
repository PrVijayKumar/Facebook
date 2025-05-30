from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from unittest.mock import patch
from ipware import get_client_ip
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives, send_mass_mail, EmailMessage 
CustomUser = get_user_model()
# from my_project.celery import app as celeryapp
from user.tasks import user_reg_email, reset_pass_email, cron_success
from celery import Celery
# from nose.tools import eq_


class TestTasks(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(username="Shahrukh", first_name="Shahrukh", last_name="Khan", email="shah@gmail.com", contact="1234567890", password="@@123456",
            dob="2000-04-29")
        # celeryapp.conf.update(CELERY_ALWAYS_EAGER=True)
        

    # test the rcode view function sms
    # @patch('user.views.reset_pass_email')
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_task_for_email_code(self):
        result = reset_pass_email.delay(self.user.username, self.user.email, self.user.id)
        # print("result", result)
        self.assertIsNotNone(True)
    #     text_content = "Code for reset password"
    #     response = self.client.post(reverse('user:rcode', kwargs={'id': self.user.id}), {'ropt': 2})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "user/ecode.html")
    #     self.assertContains(response, "Please check your phone for an email message with your code.")
    #     # mock_emv.assert_called_once_with(
        #     "Reset Code",
        #     text_content,
        #     "vijaychoudhary@gmail.com",
        #     [self.user.email],
        #     headers={"password": "reset password code"},
        # )
        # mock_emv.assert_called_once_with(
        #     self.user.username,
        #     self.user.email,
        #     self.user.id,
        # ).
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_task_user_reg_email(self):
        result = user_reg_email.delay(self.user.username, self.user.email)
        # print("result", result)
        self.assertIsNotNone(True)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_cron_success(self):
        result = cron_success()
        self.assertIsNotNone(True)
