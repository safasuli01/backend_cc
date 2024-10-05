from .models import User, OTP
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import random
from django.core.mail import send_mail
from django.utils import timezone

# Create your views here.

# class UserRegistrationView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)
#             if created:
#                 token.delete()  # Delete the token if it was already created
#                 token = Token.objects.create(user=user)
#             return Response({'token': token.key, 'username': user.username, 'role': user.role})
#         else:
#             return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
#
# class UserLogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         print(request.headers)
#         token_key = request.auth.key
#         token = Token.objects.get(key=token_key)
#         token.delete()
#
#         return Response({'detail': 'Successfully logged out'})

# View for sending OTP
class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = str(random.randint(100000, 999999))
        user, created = User.objects.get_or_create(email=email)

        # Create an OTP record
        OTP.objects.create(user=user, otp=otp_code)

        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp_code}',
            'safa.suli.2@gmail.com',
            [email],
            fail_silently=False
        )
        return Response({"message": "Please verify your account with the OTP code sent to your mail!"},
                        status=status.HTTP_200_OK)


# View for user registration
class UserRegistrationView(APIView):
    def post(self, request):
        # Create the user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate OTP
            email = request.data.get('email')
            otp_code = str(random.randint(100000, 999999))
            OTP.objects.create(user=user, otp=otp_code)

            send_mail(
                'Your OTP Code',
                f'Your OTP code is: {otp_code}',
                'safa.suli.2@gmail.com',
                [email],
                fail_silently=False
            )

            return Response({
                                "message": "User registered successfully! Please verify your account with the OTP code sent to your mail!"},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for verifying OTP during registration
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_input = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            otp_record = OTP.objects.filter(user=user).last()
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if otp_record.is_expired():
            return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.otp == otp_input:
            # Activate the user after successful OTP verification
            otp_record.delete()  # Delete the OTP record
            return Response({"message": "OTP verified successfully! You can now log in."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


# View for user login
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            return Response({'token': token.key, 'username': user.username, 'role': user.role})
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


# View for user logout
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out'})


class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the user
        user, created = User.objects.get_or_create(email=email)

        # Create an OTP record
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(user=user, otp=otp_code)

        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp_code}',
            'safa.suli.2@gmail.com',
            [email],
            fail_silently=False
        )
        return Response({"message": "Please verify your account with the OTP code sent to your mail!"},
                        status=status.HTTP_200_OK)