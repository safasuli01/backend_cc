from django.shortcuts import render
from authentication.models import User
from authentication.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from company.serializers import CompanySerializer
# from individual.serializers import IndividualSerializer
from company.models import Company
# from individual.models import Individual
from rest_framework.generics import RetrieveUpdateAPIView
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.request.user  # Get the authenticated user
        user_data = UserSerializer(user).data  # Serialize user data

        if user.role == 'company':
            try:
                # Fetch the company profile
                company = Company.objects.get(user=user)
                company_data = CompanySerializer(company).data

                # Combine user data and company-specific data
                response_data = {
                    'user': user_data,  # Include user data
                    **company_data   
                }
                return Response(response_data)

            except Company.DoesNotExist:
                return Response({'message': 'Company profile not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()  # Get the authenticated user
        serializer = self.get_serializer(user, data=request.data.get('user'), partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

# class UserLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)

#             response_data = {
#                 'token': token.key,
#             }

#             if user.role == 'company':
#                 try:
#                     company = Company.objects.get(user=user)
#                     response_data['user'] = CompanySerializer(company).data
#                 except Company.DoesNotExist:
#                     return Response({'message': 'Company profile not found'}, status=status.HTTP_404_NOT_FOUND)

#             return Response(response_data)

#         return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})






class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Generate or get the token for the user
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                'token': token.key,
            }

            # If the user is a company, fetch the company profile
            if user.role == 'company':
                try:
                    company = Company.objects.get(user=user)
                    response_data['user'] = CompanySerializer(company).data
                except Company.DoesNotExist:
                    return Response({'message': 'Company profile not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # You can add handling for other roles here if needed, or return user data
                response_data['user'] = {'username': user.username, 'email': user.email}

            return Response(response_data)

        # If authentication fails, return unauthorized response
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)