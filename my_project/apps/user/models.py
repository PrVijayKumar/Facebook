from django.db import models
import datetime
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
import logging
# uuid

logger = logging.getLogger(__name__)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(_("email address"))
    contact = models.CharField(max_length=20, null=True)
    dob = models.DateField(null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()

    def __str__(self):
        return self.email



    def get_absolute_url(self):
        return f'/user/{self.id}/'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     breakpoint()
    #     context['user'] = dict(self)
    #     return context

# class PostModel(models.Model):
#     # post_user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post_title = models.CharField(max_length=200)
#     post_date = models.DateTimeField(default=datetime.datetime.now)
#     post_content = models.ImageField(upload_to="images/")
    
#     def __str__(self):
#         return self.post_title


class Codes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name='rcode')
    code = models.CharField(max_length=10, null=True)
    CODE_CHOICES = (
            ('P', 'Phone'),
            ('E', 'Email'),
            ('W', 'Whatsapp'),
            ('F', 'Facebook')
        )
    source = models.CharField(max_length=1, choices=CODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)



class Stars(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StarsPaymentLogs(models.Model):
    sent_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="stars_sent")
    received_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="stars_received")
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    # stripe_product_id = models.CharField(max_length=100, null=True)
    # amount_in_rs = models.DecimalField(max_digits=10, decimal_places=2)
    # is_paid = models.BooleanField(default=False)
    # stripe_checkout_session_id = models.CharField(max_length=255, blank=True, null=True)
    # post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    

    # def __str__(self):
    #     return f"Stars {self.id} - {self.received_by.username}"
    
