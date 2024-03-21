# models.py

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_picture', blank=True)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_picture/')
    category = models.CharField(max_length=50)
    summary = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title
    

