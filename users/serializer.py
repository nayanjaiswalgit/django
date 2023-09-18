


from rest_framework import serializers
from .models import User

# class ProfileSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Profile
#         fields  = ['uid', 'created_at', 'profile_image', 'user']
#         depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']

class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp = serializers.CharField()

class LoginUserSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password = serializers.CharField()


