
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import ProjectSerializer
from .models import Project

# Create your views here.
class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjetSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the project (author) from the authenticated user
            serializer.save(author=request.user.individual)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all projects authored by the current user's projects
        projects = Project.objects.filter(author=request.user.project)
        serializer = ProjetSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = project.objects.get(id=project_id, author=request.user.individual)
            serializer = ProjetSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, author=request.user.individual)
            serializer = ProjetSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, author=request.user.individual)
            project.delete()
            return Response({'message': 'Project deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


