from django.db import models
from django.core.validators import RegexValidator
from authentication.models import User

# Create your models here.
    

class Individual(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('client', 'Client'),
        ('seeking', 'Seeking'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    validate_phone_validator = RegexValidator(
        regex=r'^01[0-2,5]{1}[0-9]{8}$',
        message="This is not a valid Egyptian phone number."
    )

    validate_national_id = RegexValidator(
        regex=r'^\d{14}$',
        message="National ID must be exactly 14 digits."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=14, unique=True, validators=[validate_national_id])
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    phone_number = models.CharField(max_length=11, validators=[validate_phone_validator], blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)  # Calculate from date_of_birth
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    skills = models.TextField(blank=True, null=True)  # Use a comma-separated format for multiple skills
    bio = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}"
    
    def calculate_age(self):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def save(self, *args, **kwargs):
        if self.date_of_birth:
            self.age = self.calculate_age()
        super(Individual, self).save(*args, **kwargs)
    
    