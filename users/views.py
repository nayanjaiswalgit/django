
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from base.emails import send_otp_via_email
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer, VerifyAccountSerializer, LoginUserSerializer
from .models import User
#from users.models import Profile
# from users.serializer import ProfileSerializer

# Create your views here.
# class UserList(generics.ListCreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class LoginUser(APIView):

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                user_obj = authenticate(request, email=email, password=password)

                print(user_obj.is_verified)

                if not user_obj.is_verified :
                    # Use the 'login' function to log the user in

                    return Response({
                        'status': status.HTTP_401_UNAUTHORIZED,
                        'message': 'Please Verify Account First',
                        'data': None,
                    })

                if user_obj is not None:
                    # Use the 'login' function to log the user in
                    login(request, user_obj)
                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'Login successful.',
                        'data': None,
                    })
                else:
                    return Response({
                        'status': status.HTTP_401_UNAUTHORIZED,
                        'message': 'Authentication failed. Check your email and password.',
                        'data': None,
                    })

            except User.DoesNotExist:
                return Response({
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Authentication failed. User does not exist.',
                    'data': None,
                })

        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Validation failed. Please correct the errors below.',
            'data': serializer.errors,
        })


class RegisterUser(APIView):
  
  def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp_via_email(user.email)
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Registration successful. Check your email for OTP.',
                'data': serializer.data,
            })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Something went wrong.',
            'data': serializer.errors,
        })

class VerifyOTP(APIView):
        
    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                if user.is_verified:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Account is already verified.',
                        'data': None,
                    })
                if user.otp != otp:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Please enter the correct OTP.',
                        'data': None,
                    })
                user.is_verified = True
                user.save()
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'OTP verified.',
                    'data': None,
                })
            except User.DoesNotExist:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'User not found. Register first.',
                    'data': None,
                })
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Something went wrong.',
            'data': serializer.errors,
        })
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})