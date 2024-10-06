# from rest_framework.views import APIView
# from .serializers import IndividualSerializer
# from rest_framework.response import Response
# from rest_framework import status
# from authentication.models import User
# from .models import Individual
# from django.contrib.auth import authenticate, login
# from rest_framework.views import APIView
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
#
#
#
# # Create your views here.
# class IndividualRegistrationView(APIView):
#     def post(self, request):
#         serializer = IndividualSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print(serializer.errors)  # Log the errors to debug
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # Update Login view
# class UserLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         # Fetch the username and password from the request data
#         username = request.data.get('username')  # This could be the email
#         password = request.data.get('password')
#
#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)  # Log the user in
#
#             # Get or create the token for the user
#             token, created = Token.objects.get_or_create(user=user)
#             if not created:
#                 token.delete()
#                 token = Token.objects.create(user=user)
#
#             # Prepare the response data
#             response_data = {
#                 'token': token.key,
#                 'username': user.username,
#                 'role': user.role,
#             }
#
#             return Response(response_data, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
from .models import Individual
from .serializers import IndividualSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


# Create your views here.

# Get individuals & create individual:
@api_view(['GET', 'POST'])
def list_individual(request, format=None):
    if request.method == 'GET':
        individuals = Individual.objects.all()
        serializer = IndividualSerializer(individuals, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = IndividualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Individual details, update, and delete:
@api_view(["GET", "PUT", "DELETE"])
def individual_detail(request, id):
    try:
        individual = Individual.objects.get(pk=id)
    except Individual.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  # Retrieve individual details
        serializer = IndividualSerializer(individual)
        return Response(serializer.data)

    elif request.method == 'PUT':  # Update individual
        serializer = IndividualSerializer(individual, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # Delete individual
        individual.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User Login view
@api_view(['POST'])
def user_login_view(request):
    username = request.data.get('username')  # Could be the email
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)  # Log the user in

        # Get or create the token for the user
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            token = Token.objects.create(user=user)

        # Prepare the response data
        response_data = {
            'token': token.key,
            'username': user.username,
            'role': user.role,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
