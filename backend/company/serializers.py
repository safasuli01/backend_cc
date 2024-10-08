# rest_frameworkfrom rest_framework import serializers
# from .models import Company
# from authentication.serializers import UserSerializer
# from authentication.models import User
#
# class CompanySerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=False)  # Make user field optional
#
#     class Meta:
#         model = Company
#         fields = '__all__'
#         extra_kwargs = {
#             'registration_documents': {'required': False},
#             'logo': {'required': False},
#         }
#
#
#     def create(self, validated_data):
#         user_data = validated_data.pop('user', None)  # Use pop with default None
#         user = None
#
#         # Create user only if user_data is provided
#         if user_data:
#             user = User.objects.create_user(**user_data)
#
#         # Create the company instance
#         company = Company.objects.create(user=user, **validated_data)
#         return company
#
#     def update(self, instance, validated_data):
#         user_data = validated_data.pop('user', None)
#
#         # Update user only if user_data is provided
#         if user_data:
#             user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
#             user_serializer.is_valid(raise_exception=True)
#             user_serializer.save()
#
#         # Update the company instance with the rest of the validated data
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#
#         instance.save()
#         return instance

from rest_framework import serializers
from authentication.models import User
from authentication.serializers import UserSerializer
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'company'
        user = User.objects.create_user(**user_data)

        company = Company.objects.create(user=user, **validated_data)

        return company
