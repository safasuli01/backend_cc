from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import JobSerializer
from .models import Job
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def job_create(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user.company)  # Set the author to the current user's company
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_list(request):
    # permission_classes = [IsAuthenticated]
    if request.method == 'GET':
        # Get all jobs authored by the current user's company
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def job_detail(request, id):
    try:
        # Retrieve the job by the given ID
        job = Job.objects.get(pk=id)
    except Job.DoesNotExist:
        # Return a 404 if the job is not found
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the job object and return the data
    serializer = JobSerializer(job)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def job_update(request, id):
    try:
        job = Job.objects.get(pk=id)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if job.author != request.user.company:  # Check if the user is the author
        return Response({'detail': 'You do not have permission to edit this job.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = JobSerializer(job, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def job_delete(request, id):
    print(f"Authenticated User: {request.user}")  # Debugging line
    try:
        job = Job.objects.get(pk=id)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if job.author != request.user.company:  # Check if the user is the author
        return Response({'detail': 'You do not have permission to delete this job.'}, status=status.HTTP_403_FORBIDDEN)

    job.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# serch view by location&title
@api_view(['GET'])
def search_job(request):
    title = request.query_params.get('title', None)
    location = request.query_params.get('location', None)
    jobs = Job.objects.all()
    if title:
        jobs = jobs.filter(title__icontains=title)
    if location:
        jobs = jobs.filter(location__icontains=location)

    # Serialize the filtered companies
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)