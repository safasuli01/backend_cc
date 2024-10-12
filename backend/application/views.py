from django.shortcuts import render
from .models import Proposal
from .serializers import ProposalSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ProposalCreateView(generics.CreateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

class ProposalListView(generics.ListAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        individual = getattr(user, 'individual', None)
        company = getattr(user, 'company', None)

        if individual:
            return Proposal.objects.filter(individual=individual)
        elif company:
            return Proposal.objects.filter(company=company)
        return Proposal.objects.none()