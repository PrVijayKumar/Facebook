from celery import shared_task
from time import sleep
from django.core.mail import send_mail, EmailMultiAlternatives, send_mass_mail, EmailMessage
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from email.mime.image import MIMEImage
# from django.contrib.auth.models import User
from user.models import CustomUser, Codes
from datetime import datetime
from testing.models import DemoTable
import json
import random, string
from django.template.loader import render_to_string





@shared_task
def reset_pass_email(username, email, id):
    rcode = f"{random.randrange(99999999):08}"
    # print(type(f"{random.randrange(99999999):08}"))
    # try:
    #     codes = Codes.objects.filter(user_id=int(id))
    #     for c in codes:
    #         c.delete()
    # except(Codes.DoesNotExist):
    #     pass
    code = Codes(user_id=int(id), source='E', code=rcode)
    code.save()

    text_content = "Code for reset password"

    html_content = render_to_string(
        "../templates/user/passmail.html",
        context={"code": rcode},
    )

    msg = EmailMultiAlternatives(
        "Reset Code",
        text_content,
        "vijaychoudhary@gmail.com",
        [email],
        headers={"password": "reset password code"},
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()



@shared_task
def user_reg_email(username, email):
    send_mail(
        "Welcome to Facebook Clone!",
        f"Hy {username}, Connect with your friends and communities with Facebook Clone Project.",
        "vijaychoudhary@thoughtwin.com",
        [email],
        fail_silently=False
    )
    return 'sent'


def cron_success():
    print("Hello from crontab")

# Create Schedule Every Day at 10 AM
# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=1,
#     period=IntervalSchedule.DAYS,
# )


# Creating the Crontab Schedule every day at 10 AM
# schedule, _ = CrontabSchedule.objects.get_or_create(
#         minute="*",
#         hour="*",
#         day_of_week="*",
#         day_of_month="*",
#         month_of_year="*",
#     )


# # Schedule the periodic task programmatically
# PeriodicTask.objects.get_or_create(
#     crontab=schedule,
#     name='Birthday Wish',
#     task='users.tasks.birthday_wishes',
#     # args=json.dumps(['Happy Birthday']),
# )


# print(mytask)

