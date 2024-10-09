# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Company
# from .serializers import CompanySerializer
# from rest_framework.permissions import IsAuthenticated
#
# from rest_framework.permissions import AllowAny  # Import AllowAny permission
#
# # Get companies & create company:
# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])  # Allow unauthenticated access for GET requests
# def list_company(request):
#     if request.method == 'GET':
#         companies = Company.objects.all()
#         serializer = CompanySerializer(companies, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = CompanySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # Retrieve company details
# @api_view(['GET'])
# def company_detail(request, id):
#     company = get_object_or_404(Company, pk=id)
#     serializer = CompanySerializer(company)
#     return Response(serializer.data)
#
# # Update company
# @api_view(['PUT'])
# def update_company(request, id):
#     company = get_object_or_404(Company, pk=id)
#     serializer = CompanySerializer(company, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # Delete company
# @api_view(['DELETE'])
# def delete_company(request, id):
#     company = get_object_or_404(Company, pk=id)
#     company.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['POST'])
# @permission_classes([AllowAny])  # Allow unauthenticated access for login
# def company_login_view(request):
#     username = request.data.get('username')  # Username (could also be email)
#
#     # Authenticate the user
#     user = authenticate(request, username=username)
#
#     if user is not None:
#         # Ensure the user has an associated company
#         try:
#             company = Company.objects.get(user=user)
#         except Company.DoesNotExist:
#             return Response({'message': 'No company associated with this user.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         login(request, user)  # Log the user in
#
#         # Get or create the token for the user
#         token, created = Token.objects.get_or_create(user=user)
#         if not created:
#             token.delete()
#             token = Token.objects.create(user=user)
#
#         # Prepare the response data with company details
#         response_data = {
#             'token': token.key,
#             'username': user.username,
#             'company_name': company.company_name,
#             'industry': company.industry,
#             'location': company.location,
#             'role': user.role if hasattr(user, 'role') else None,
#         }
#
#         return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
#
# # Search view for companies by company_name, location, and industry
# @api_view(['GET'])
# @permission_classes([AllowAny])  # Allow unauthenticated access for searching
# def search_company(request):
#     company_name = request.query_params.get('company_name', None)
#     location = request.query_params.get('location', None)
#     industry = request.query_params.get('industry', None)
#
#     companies = Company.objects.all()
#
#     if company_name:
#         companies = companies.filter(company_name__icontains=company_name)
#     if location:
#         companies = companies.filter(location__icontains=location)
#     if industry:
#         companies = companies.filter(industry__icontains=industry)
#
#     # Serialize the filtered companies
#     serializer = CompanySerializer(companies, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

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
from .models import Company
from  .serializers import *
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
    activation_link = request.build_absolute_uri(reverse('activate-company', kwargs={'uidb64': uid}))
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


class CompanyRegistrationView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            send_activation_email(user, request)
            messages.success(request, f'Dear {user.user.username}, please go to your email inbox and click on the received activation link to confirm and complete the registration. Check your spam folder if necessary.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access for searching
def search_company(request):
    # user_name = request.query_params.get('company_name', None)
    location = request.query_params.get('location', None)
    industry = request.query_params.get('industry', None)

    companies = Company.objects.all()

    if company_name:
        companies = companies.filter(company_name__icontains=company_name)
    if location:
        companies = companies.filter(location__icontains=location)
    if industry:
        companies = companies.filter(industry__icontains=industry)

    # Serialize the filtered companies
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get allcompanies :
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access for GET requests
def list_company(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)