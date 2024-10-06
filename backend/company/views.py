# from django.shortcuts import render
# from rest_framework.views import APIView
# from .serializers import CompanySerializer
# from rest_framework.response import Response
# from rest_framework import status
# from authentication.models import User
# from .models import Company
# from django.contrib.auth import authenticate, login
# from rest_framework.views import APIView
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
#
#
# # Create your views here.
# class CompanyRegistrationView(APIView):
#     def post(self, request):
#         serializer = CompanySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # Update Login view
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
#
#             response_data = {
#                 'token': token.key,
#                 'username': user.username,
#                 'role': user.role,
#             }
#
#             if user.role == 'student':
#                 student = user.student_account  # Assuming the related name is "student_account"
#                 if student is not None:
#                     # Add student data to the response data
#                     individual_data = CompanySerializer(company).data
#                     response_data['data'] = individual_data
#
#             return Response(response_data)
#         else:
#             return Response({'message': 'Invalid username or password'})

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Get companies & create company:
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_company(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Company details, update, and delete:
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def company_detail(request, id):
    company = get_object_or_404(Company, pk=id)

    if request.method == 'GET':  # Retrieve company details
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    elif request.method == 'PUT':  # Update company
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # Delete company
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# User Login view allowing token retrieval with only the username
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        # Use get_user_model() to get the user model
        User = get_user_model()
        user = User.objects.filter(username=username).first()

        if user is not None:
            # Create or retrieve the token for the user
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
