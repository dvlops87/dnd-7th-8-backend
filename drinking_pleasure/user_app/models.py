from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.utils import timezone
# Create your views here.

class UserManager(BaseUserManager):
    pass

class User(AbstractBaseUser):
    objects = UserManager()
    customer_uuid = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(default='',max_length=50)
    profile = models.ImageField(upload_to="user-img/", blank=True, null=True)
    birth = models.DateField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email
