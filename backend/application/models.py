from django.db import models
from individual.models import Individual
from company.models import Company
from job.models import Job
from project.models import Project

# Create your models here.
class Proposal(models.Model):
    individual = models.ForeignKey(Individual,on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.individual:
            return f"Proposal by {self.individual.first_name} {self.individual.last_name} to Job {self.job.title}"
        return f"Proposal by {self.company.user} to Project {self.project.title}"
