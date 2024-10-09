# # from rest_framework.views import APIView
# # from .serializers import IndividualSerializer
# # from rest_framework.response import Response
# # from rest_framework import status
# # from authentication.models import User
# # from .models import Individual
# # from django.contrib.auth import authenticate, login
# # from rest_framework.views import APIView
# # from rest_framework.authtoken.views import ObtainAuthToken
# # from rest_framework.authtoken.models import Token
# # from rest_framework.permissions import IsAuthenticated
# #
# #
# #
# # # Create your views here.
# # class IndividualRegistrationView(APIView):
# #     def post(self, request):
# #         serializer = IndividualSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         print(serializer.errors)  # Log the errors to debug
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # # Update Login view
# # class UserLoginView(ObtainAuthToken):
# #     def post(self, request, *args, **kwargs):
# #         # Fetch the username and password from the request data
# #         username = request.data.get('username')  # This could be the email
# #         password = request.data.get('password')
# #
# #         # Authenticate the user
# #         user = authenticate(request, username=username, password=password)
# #         if user is not None:
# #             login(request, user)  # Log the user in
# #
# #             # Get or create the token for the user
# #             token, created = Token.objects.get_or_create(user=user)
# #             if not created:
# #                 token.delete()
# #                 token = Token.objects.create(user=user)
# #
# #             # Prepare the response data
# #             response_data = {
# #                 'token': token.key,
# #                 'username': user.username,
# #                 'role': user.role,
# #             }
# #
# #             return Response(response_data, status=status.HTTP_200_OK)
# #         else:
# #             return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
#
# from .models import Individual
# from .serializers import IndividualSerializer
# from django.http import JsonResponse
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from authentication.models import User
# from django.contrib.auth import authenticate, login
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
#
#
# # Create your views here.
#
# # Get individuals & create individual:
# @api_view(['GET', 'POST'])
# def list_individual(request, format=None):
#     if request.method == 'GET':
#         individuals = Individual.objects.all()
#         serializer = IndividualSerializer(individuals, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         print("Received data:", request.data)
#         serializer = IndividualSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print("Errors:", serializer.errors)  # Print the validation errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # Individual details, update, and delete:
# @api_view(["GET", "PUT", "DELETE"])
# def individual_detail(request, id):
#     try:
#         individual = Individual.objects.get(pk=id)
#     except Individual.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':  # Retrieve individual details
#         serializer = IndividualSerializer(individual)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':  # Update individual
#         serializer = IndividualSerializer(individual, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':  # Delete individual
#         individual.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# # User Login view
# @api_view(['POST'])
# def user_login_view(request):
#     username = request.data.get('username')  # Could be the email
#     password = request.data.get('password')
#
#     # Authenticate the user
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)  # Log the user in
#
#         # Get or create the token for the user
#         token, created = Token.objects.get_or_create(user=user)
#         if not created:
#             token.delete()
#             token = Token.objects.create(user=user)
#
#         # Prepare the response data
#         response_data = {
#             'token': token.key,
#             'username': user.username,
#             'role': user.role,
#         }
#
#         return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
#
#
#
#
#
# # from .models import Individual
# # from .serializers import IndividualSerializer
# # from rest_framework import status
# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from rest_framework.permissions import IsAuthenticated
# # from django.contrib.auth import authenticate, login
# # from rest_framework.authtoken.models import Token
#
# # # Create your views here.
#
# # @api_view(['GET', 'POST'])
# # def list_individual(request):
# #     if request.method == 'GET':
# #         individuals = Individual.objects.all()
# #         serializer = IndividualSerializer(individuals, many=True)
# #         return Response(serializer.data)
#
# #     elif request.method == 'POST':
# #         print("Received data:", request.data)  # Log incoming request data
# #         serializer = IndividualSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         print("Errors:", serializer.errors)  # Log validation errors
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # @api_view(["GET", "PUT", "DELETE"])
# # def individual_detail(request, id):
# #     try:
# #         individual = Individual.objects.get(pk=id)
# #     except Individual.DoesNotExist:
# #         return Response(status=status.HTTP_404_NOT_FOUND)
#
# #     if request.method == 'GET':
# #         serializer = IndividualSerializer(individual)
# #         return Response(serializer.data)
#
# #     elif request.method == 'PUT':
# #         serializer = IndividualSerializer(individual, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# #     elif request.method == 'DELETE':
# #         individual.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
#
# # @api_view(['POST'])
# # def user_login_view(request):
# #     username = request.data.get('username')  # Could be the email
# #     password = request.data.get('password')
#
# #     # Authenticate the user
# #     user = authenticate(request, username=username, password=password)
# #     if user is not None:
# #         login(request, user)  # Log the user in
#
# #         # Get or create the token for the user
# #         token, created = Token.objects.get_or_create(user=user)
#
# #         # Prepare the response data
# #         response_data = {
# #             'token': token.key,
# #             'username': user.username,
# #             'role': user.role,  # Make sure 'role' exists on User model
# #         }
#
# #         return Response(response_data, status=status.HTTP_200_OK)
# #     else:
# #         return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render, redirect
from rest_framework import viewsets, status,permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Individual
from .serializers import *
from .models import *
from authentication.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def send_activation_email(user, request):
    subject = "CareerConnect Account Activation"
    uid = urlsafe_base64_encode(force_bytes(user.user.pk))
    print("uid",uid)
    activation_link = request.build_absolute_uri(reverse('activate-individual', kwargs={'uidb64': uid}))
    message = f"Hello {user.user.username}, please click the link to activate your account: {activation_link}"

    send_mail(
        subject,
        message,
        'CareerConnect <safa.suli.2@gmail.com>',
        [user.user.email],
        fail_silently=False,
    )
def activate(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been successfully activated!')
        return redirect('http://localhost:3000/signin')
    except User.DoesNotExist:
        print(request)
        messages.error(request, 'Invalid activation link')
        return redirect('http://localhost:3000/signup')


class IndividualRegistrationView(APIView):
    def post(self, request):
        serializer = IndividualSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            send_activation_email(user, request)
            messages.success(request, f'Dear {user.user.username}, please go to your email inbox and click on the received activation link to confirm and complete the registration. Check your spam folder if necessary.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


api_view(['GET'])
def search_individual(request):
    username = request.query_params.get('username', None)
    specialization = request.query_params.get('specialization', None)

    individuals = Individual.objects.all()

    if username:
        # Filter by username
        individuals = individuals.filter(user__username__icontains=username)

    if specialization:
        # Filter by specialization
        individuals = individuals.filter(specialization__icontains=specialization)

    serializer = IndividualSerializer(individuals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get all individual :
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access for GET requests
def list_individual(request):
    if request.method == 'GET':
        individuals = Individual.objects.all()
        serializer = IndividualSerializer(individuals, many=True)
        return Response(serializer.data)