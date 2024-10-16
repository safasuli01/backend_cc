from django.db import models
from company.models import Company


# Create your models here.
class Job(models.Model):
    STATUS = (
        ("active", "Active"),
        ("disabled", "Disabled"),
    )
    JOB_TYPE_CHOICES = [
        ('part_time', 'Part Time'),
        ('full_time', 'Full Time'),
        ('remote', 'Remote'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    industry = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    post_status = models.CharField(max_length=100, choices=STATUS, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200,  blank=True, null=True)
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, blank=True, null=True)
    salary = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title