from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,email=None,password=None,**extra_fields):

        if not email:
            raise ValueError('The Email field must be set')
        email=self.normalize_email(email=email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email=email,password=password,**extra_fields)
class CustomUser(AbstractUser):
    pateint=1
    doctor=2
    counselor=3
    manager=4
    role_choice=(
        ("patient",'patient'),
        ("doctor",'doctor'),
        ("counselor",'counselor'),
        ("manager",'manager')
    )
    email=models.EmailField(unique=True,max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role=models.CharField(choices=role_choice,max_length=50,default='patient')
    phonenumber=models.CharField(max_length=50,blank=True,null=True)
    birth=models.DateField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    registrationnumber=models.CharField(max_length=50,blank=True,null=True)
    username = models.CharField(max_length=50,unique=False)
    objects =CustomUserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

