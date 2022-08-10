from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    pass

class MazleUser(AbstractBaseUser):
    objects = UserManager()
    customer_uuid = models.AutoField(primary_key=True, unique=True)
    email = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=50)
    passwd = models.CharField(max_length=255)
    birth = models.DateField()
    profile = models.TextField(blank=True, null=True)
    platform = models.CharField(max_length=10)

    USERNAME_FIELD='email'

    class Meta:
        managed = True
        db_table = 'mazle_user'


class MazleUserConsent(models.Model):
    customer_uuid = models.CharField(primary_key=True, max_length=40)
    consent = models.IntegerField()
    update_dtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mazle_user_consent'

