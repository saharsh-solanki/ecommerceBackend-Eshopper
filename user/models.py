from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from user.manager import CustomUserManager


class SiteUser(AbstractUser):
    username = None
    email = models.CharField(max_length=30,unique=True)
    mobile_number = models.PositiveBigIntegerField(null=True,blank=True,max_length=12)
    profile_image = models.ImageField(upload_to="media/profile_images/",default="media/profile_images/deafult_user_image.png",null=True,blank=True)
    last_name = None
    first_name = None
    name = models.CharField(max_length=100,default="User")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
