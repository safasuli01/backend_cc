from rest_framework import serializers
from .models import Individual
from backend.authentication.serializers import UserSerializer

class IndividualSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Individual
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        individual = Individual.objects.create(user=user, **validated_data)
        return individual
