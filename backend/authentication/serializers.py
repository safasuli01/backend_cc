# # from rest_framework import serializers
# # from .models import User, OTP
# #
# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = ['first_name', 'last_name', 'username', 'password', 'email', 'role']
# #         extra_kwargs = {'password': {'write_only': True, 'required': True}}
# #
# #     def create(self, validated_data):
# #         user = User(
# #             username=validated_data['username'],
# #             email=validated_data['email'],
# #             first_name=validated_data['first_name'],
# #             last_name=validated_data['last_name'],
# #             role=validated_data['role']
# #         )
# #         user.set_password(validated_data['password'])
# #         user.save()
# #         return user
# #
# # class OTPSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = OTP
# #         fields = ['otp']
#
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings
# from rest_framework.authtoken.models import Token
#
# # Create your models here.
#
#
# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('individual', 'Individual'),
#         ('company', 'Company')
#     )
#     is_active= models.BooleanField(default=False)
#     email = models.EmailField(unique=True)
#     role = models.CharField(max_length=15, choices=ROLE_CHOICES)
#
#     def save(self, *args, **kwargs):
#         if self.is_superuser:
#             self.is_active = True
#         super().save(*args, **kwargs)

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user