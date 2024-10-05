
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import ProjectSerializer
from .models import Project
from rest_framework.decorators import api_view

# Create your views here.
class ProjectCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the project (author) from the authenticated user
            serializer.save(author=request.user.individual)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def project_list(request):
    # permission_classes = [IsAuthenticated]
    if request.method == 'GET':
        # Get all projects authored by the current user's company
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET'])
def project_detail(request, id):
    try:
        # Retrieve the project by the given ID
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        # Return a 404 if the project is not found
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the project object and return the data
    serializer = ProjectSerializer(project)
    return Response(serializer.data)

@api_view(['PUT'])
def project_update(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def project_delete(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
