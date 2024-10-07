from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import AllowAny  # Import AllowAny permission

# Get companies & create company:
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access for GET requests
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

# Retrieve company details
@api_view(['GET'])
def company_detail(request, id):
    company = get_object_or_404(Company, pk=id)
    serializer = CompanySerializer(company)
    return Response(serializer.data)

# Update company
@api_view(['PUT'])
def update_company(request, id):
    company = get_object_or_404(Company, pk=id)
    serializer = CompanySerializer(company, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete company
@api_view(['DELETE'])
def delete_company(request, id):
    company = get_object_or_404(Company, pk=id)
    company.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access for login
def company_login_view(request):
    username = request.data.get('username')  # Username (could also be email)

    # Authenticate the user
    user = authenticate(request, username=username)
    
    if user is not None:
        # Ensure the user has an associated company
        try:
            company = Company.objects.get(user=user)
        except Company.DoesNotExist:
            return Response({'message': 'No company associated with this user.'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)  # Log the user in

        # Get or create the token for the user
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            token = Token.objects.create(user=user)

        # Prepare the response data with company details
        response_data = {
            'token': token.key,
            'username': user.username,
            'company_name': company.company_name,
            'industry': company.industry,
            'location': company.location,
            'role': user.role if hasattr(user, 'role') else None,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

# Search view for companies by company_name, location, and industry
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access for searching
def search_company(request):
    company_name = request.query_params.get('company_name', None)
    location = request.query_params.get('location', None)
    industry = request.query_params.get('industry', None)

    companies = Company.objects.all()

    if company_name:
        companies = companies.filter(company_name__icontains=company_name)
    if location:
        companies = companies.filter(location__icontains=location)
    if industry:
        companies = companies.filter(industry__icontains=industry)

    # Serialize the filtered companies
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
