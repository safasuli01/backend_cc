from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('individual', 'Individual'),
        ('company', 'Company')
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True) 
    last_name = models.CharField(max_length=200, blank=True, null=True)


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
