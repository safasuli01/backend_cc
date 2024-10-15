from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import ProjectSerializer
from .models import Project
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    name = 'project-list'

    filter_fields = (
        'industry'
    )


@api_view(['POST'])
def project_create(request):
    serializer = ProjectSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # Check if the user is authenticated and has an associated individual profile
        if request.user.is_authenticated and hasattr(request.user, 'individual'):
            # Assign the individual as the author
            serializer.save(author=request.user.individual)
        else:
            # Temporarily handle cases where no user is logged in
            return Response({"detail": "User must be authenticated and have an individual profile."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def project_list(request):
    # permission_classes = [IsAuthenticated]
    if request.method == 'GET':
        # Get all projects authored by the current user's company
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)



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
@permission_classes([IsAuthenticated])
def project_update(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure only the author can update the project
    if project.author != request.user.individual:
        return Response({'error': 'You do not have permission to edit this project.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def project_delete(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure only the author can delete the project
    if project.author != request.user.individual:
        return Response({'error': 'You do not have permission to delete this project.'},
                        status=status.HTTP_403_FORBIDDEN)

    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)