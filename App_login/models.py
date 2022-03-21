from dataclasses import field
from email.policy import default
from lib2to3.pgen2.token import RIGHTSHIFT
from operator import mod
from pyexpat import model
from re import T
import re
from tkinter.messagebox import RETRY
from turtle import right
from django.db import models

#to create a custom model and admin panel

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy

#to automaticali create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class MyUserManager(BaseUserManager):

    """ a custom managger to deal with emails as uniqe indenter"""
    def _create_user(self, email, password, **extra_fields):

        """ Createand save user with given emails and password """

        if not email:
            raise ValueError ("This Email must be set!")
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default = False,
        help_text = ugettext_lazy('Designates whether the user can log in this site')

    )

    is_active = models.BooleanField(
        ugettext_lazy('active'),
        default=True,
        help_text=ugettext_lazy('Designates wether this user should be trated as active. Unseleted of deleting account')
    )
    USERNAME_FIELD='email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300,blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_joind = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.username + "'s Profile"

    def is_fully_filled(self):
        fields_names=[f.name for f in self._meta.get_fields()]
        
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

@receiver(post_save, sender=User)
def create_profile(sender, instance, created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()





