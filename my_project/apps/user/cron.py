from testing.models import DemoTable
from datetime import datetime
from django.utils import timezone
# from user.models import User
from user.models import CustomUser
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
import pathlib
# @shared_task
def birthday_wishes():
    # print("Happy Birthday")
    # breakpoint()
    # f = open('/home/thoughtwin/vijay/avdojo.txt', 'w')
    # f.close()
    # inst = DemoTable.objects.create(name="Birthday", about="Birthday Boy", siblings=3, marks=50, indian=True, dob="2001-01-01", email="birthday@gmail.com", password1="Birthday@@123", city="Neemuch", created_at=timezone.now()
    # inst.save()
    # users = User.objects.filter(date_joined__range = ["2025-03-19", "2025-03-20"])
    print(timezone.today())
    users = CustomUser.objects.filter(date_joined__gt = timezone.today())
    # users = User.objects.filter(date_joined__gt = timezone.today())
    # users = User.objects.filter(email="vijay24082000@gmail.com")
    # fields = User._meta.get_fields()
    # print(fields)
    for user in users:
        print("Happy Birthday")
        print("User Email:", user.email)
        print("User Name:", user.first_name)
        email = EmailMessage(
            f"Happy Birthday, {user.first_name}",
            f"Dear {user.first_name}, Facebook Clone Team hope your birthday is filled with wonderful memories and a year ahead filled with success!",
            "vijaychoudhary@thoughtwin.com",
            [user.email],
            reply_to=["vijaychoudhary@thoughtwin.com"],
            headers={"My-Header": "This is a Header"}
        )
        path = pathlib.Path(__file__).parent.parent.parent.resolve()/'media/images'/'birthday.jpeg'
        print(path)
        img_data = open(path, 'rb').read()
        msgImg = MIMEImage(img_data, 'png')
        email.attach(msgImg)
        num = email.send(fail_silently=False)
        print(num)


    # users = User.objects.filter(date_joined.date() == "2025-03-19")
    # print(users)
    # for user in users:
    #     # print(user.name)
    #     print(user.email)
        # email = EmailMessage(
        #         f"Happy Birthday, {user.first_name}"
        #         f"Dear {user.first_name}, I hope your birthday is filled with wonderful memories and a year ahead filled with success!",
        #         "vijaychoudhary@thoughtwin.com",
        #         [user.email],
        #         reply_to="vijaychoudhary@thoughtwin.com",
        #         headers={"My-Header": "This is a Header"}

        #     )

        # path = pathlib.Path(__file__).parent.parent.parent.resolve()/'media/images'/'449195169_1720433388491215_1556072659052802667_n_2axw1hM.png'
        # img_data = open(path, 'rb').read()
        # msgImg = MIMEImage(img_data, 'png')
        # email.attach(msgImg)
        # num = email.send(fail_silently=False)
        # print(num)
