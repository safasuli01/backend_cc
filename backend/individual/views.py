from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import IndividualSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class IndividualRegistrationView(APIView):
    def post(self, request):
        serializer = IndividualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Login view
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

            response_data = {
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }

            if user.role == 'student':
                student = user.student_account  # Assuming the related name is "student_account"
                if student is not None:
                    # Add student data to the response data
                    individual_data = IndividualSerializer(individual).data
                    response_data['data'] = individual_data

            return Response(response_data)
        else:
            return Response({'message': 'Invalid username or password'})
