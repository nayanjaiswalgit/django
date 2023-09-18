#from .models import Profile
from django.contrib import admin

from users.models import User

# Register your models here.
admin.site.register(User)