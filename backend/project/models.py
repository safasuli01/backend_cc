from django.db import models
from individual.models import Individual


# Create your models here.
class Project(models.Model):
    STATUS = (
        ("active", "Active"),
        ("disabled", "Disabled"),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    industry = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Individual, on_delete=models.CASCADE, null=True)
    post_status = models.CharField(max_length=100, choices=STATUS, default="Active", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title
