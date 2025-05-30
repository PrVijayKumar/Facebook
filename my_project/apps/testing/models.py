from django.db import models
from django.utils import timezone
# Create your models here.


class DemoTable(models.Model):
    name = models.CharField(max_length=255, null=True)
    about = models.TextField()
    siblings = models.IntegerField(default=5)
    marks = models.FloatField()
    indian = models.BooleanField()
    dob = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    password1 = models.CharField(max_length=20)
    city = models.CharField(max_length=50, null=True)