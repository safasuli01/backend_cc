
from django.shortcuts import render, redirect
from rest_framework import viewsets, status,permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
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
        return redirect('http://localhost:3000/login') 
    except User.DoesNotExist:
        print(request)
        messages.error(request, 'Invalid activation link')
        return redirect('http://localhost:3000/register/company')


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
@permission_classes([AllowAny])  # Allow public access to view any company's profile
def get_company_profile(request, id=None):
    try:
        if id:
            company = Company.objects.get(pk=id)  # Fetch company by ID
        else:
            company = request.user.company  # Fetch the logged-in user's company

        jobs = company.job_set.all()
        job_data = [{'id': job.id, 'title': job.title} for job in jobs]

        data = {
            'id': company.id,
            'user': {
                'username': company.user.username,
                'email': company.user.email,
            },
            'logo': company.logo.url if company.logo else None,
            'bio': company.bio,
            'industry': company.industry,
            'jobs': job_data,
        }
        return Response(data)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)



@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access for searching
def search_company(request):
    # user_name = request.query_params.get('company_name', None)
    company_name = request.query_params.get('company_name', None)  # Renamed from user_name to company_name for clarity
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



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def company_update(request, id):
    try:
        company = Company.objects.get(pk=id)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if company.user != request.user:
        return Response({'detail': 'You do not have permission to edit this profile.'},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = CompanySerializer(company, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def company_delete(request, id):
    try:
        company = Company.objects.get(pk=id)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Ensure that the user is the owner of the profile
    if company.user != request.user:
        return Response({'detail': 'You do not have permission to delete this profile.'},
                        status=status.HTTP_403_FORBIDDEN)

    company.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

