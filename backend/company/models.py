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
    company_name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to="company_logos", blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    registration_id = models.CharField(max_length=14, unique=True)
    registration_document = models.FileField(upload_to='company_documents/', blank=True, null=True)
    phone_number = models.CharField(max_length=11, validators=[validate_phone_validator], blank=True, null=True)
    location = models.CharField(max_length=200)
    company_type = models.BooleanField(default=False, help_text="Select if the company is client based or not .")

    def __str__(self):
        return f"{self.company.company_name}"
