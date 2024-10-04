from rest_framework import serializers
from .models import Individual
from authentication.serializers import UserSerializer
from authentication.models import User

class IndividualSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Individual
        fields = ['user', 'date_of_birth', 'gender', 'phone_number', 'specialization', 'national_id', 'account_type']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()  # Create and save the User object

        individual = Individual.objects.create(user=user, **validated_data)
        return individual
