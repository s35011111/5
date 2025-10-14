from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField  # pip install django-countries




class CustomUser(AbstractUser):
    email=models.EmailField(blank=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    country = CountryField(blank=True, null=True)


    def __str__(self):
        return self.username