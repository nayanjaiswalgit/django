from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User


from django.contrib.auth.models import AbstractUser, User

from users.manager import UserManager
# class Profile(BaseModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     is_email_verified = models.BooleanField(default=False)
#     email_token = models.CharField(max_length=100, null=True, blank=True)
#     profile_image = models.ImageField(upload_to='profile')

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def name(self):
        return self.first_name + ' '+self.last_name
    
    def __str__(self):
        return self.email








