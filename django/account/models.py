from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=255,unique=True)

class ValidationCode(models.Model):
    mobile = models.CharField(max_length=11,null=True,blank=True)
    validation_code = models.CharField(max_length=5,null=True,blank=True)
    time_created = models.DateTimeField(null=True,blank=True)

  


