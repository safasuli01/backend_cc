from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import JobSerializer
from .models import Job

# Create your views here.
class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the company (author) from the authenticated user
            serializer.save(author=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all jobs authored by the current user's company
        jobs = Job.objects.filter(author=request.user.company)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class JobDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, author=request.user.company)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, author=request.user.company)
            serializer = JobSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, author=request.user.company)
            job.delete()
            return Response({'message': 'Job deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

