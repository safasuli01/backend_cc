from rest_framework import serializers
from .models import Proposal
from individual.models import Individual
from company.models import Company

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['id', 'individual', 'company', 'job', 'project', 'message', 'created_at']

    def validate(self, data):
        individual = data.get('individual')
        company = data.get('company')
        job = data.get('job')
        project = data.get('project')

        #Individuals with 'seeking' role can apply only to jobs
        if individual:
            if individual.account_type != 'seeking':
                raise serializers.ValidationError("Only individuals with role 'seeking' can apply for jobs.")
            if not job:
                raise serializers.ValidationError("An individual must apply to a job.")
            if company or project:
                raise serializers.ValidationError("Individuals cannot apply to projects or on behalf of companies.")

        #Companies can apply only to projects
        if company:
            if not project:
                raise serializers.ValidationError("A company must apply to a project.")
            if individual or job:
                raise serializers.ValidationError("Companies cannot apply to jobs or on behalf of individuals.")

        return data
