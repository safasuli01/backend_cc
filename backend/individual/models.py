from django.db import models
from django.core.validators import RegexValidator
from authentication.models import User

# Create your models here.
class Individual(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('hiring','Hiring'),
        ('seeking','Seeking'),
    ]

    GENDER_CHOICES = [
        ('male','Male'),
        ('female','Female'),
    ]

    validate_phone_validator = RegexValidator(
        regex=r'^01[0-2,5]{1}[0-9]{8}$',
        message="This is not a valid Egyptian phone number."
    )

    validate_nid_validator = RegexValidator(
        regex=r'^01[0-2,5]{1}[0-9]{8}$',
        message="This is not a valid Egyptian phone number."
    )

    validate_national_id = RegexValidator(
        regex=r'^\d{14}$',
        message="National ID must be exactly 14 digits."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=14, unique=True, validators=validate_national_id)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    phone_number = models.CharField(max_length=11, validators=[validate_phone_validator], blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"  # Corrected access to user fields
