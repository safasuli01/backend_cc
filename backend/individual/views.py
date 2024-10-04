from rest_framework.views import APIView
from .serializers import IndividualSerializer
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from .models import Individual
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated



# Create your views here.
class IndividualRegistrationView(APIView):
    def post(self, request):
        serializer = IndividualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Log the errors to debug
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Login view
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Fetch the username and password from the request data
        username = request.data.get('username')  # This could be the email
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
