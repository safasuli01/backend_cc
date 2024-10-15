
from rest_framework import serializers
from .models import Individual
from authentication.serializers import UserSerializer

class IndividualSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # Make user field optional

    class Meta:
        model = Individual
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        individual = Individual.objects.create(user=user, **validated_data)
        return individual

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        # Update user only if user_data is provided
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Update the individual instance with the rest of the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
