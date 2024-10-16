from django.db import models
from django.core.validators import RegexValidator
from authentication.models import User

# Create your models here.
class Company(models.Model):
    validate_phone_validator = RegexValidator(
        regex=r'^01[0-2,5]{1}[0-9]{8}$',
        message="This is not a valid Egyptian phone number."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    industry = models.CharField(max_length=100, blank=True, null=True)
    registration_id = models.CharField(max_length=14, unique=True, blank=True, null=True)
    registration_documents = models.FileField(upload_to='registration_docs/', blank=True, null=True)
    phone_number = models.CharField(max_length=11, validators=[validate_phone_validator], blank=True, null=True)
    location = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="company_logos", blank=True, null=True)
    cover = models.ImageField(upload_to="company_cover", blank=True, null=True)
    client_base = models.BooleanField(default=False, help_text="Select if the company is client based or not .")
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    company_size = models.CharField(max_length=50, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], blank=True, null=True)
    founded = models.DateField(blank=True, null=True)
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    employees = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"
