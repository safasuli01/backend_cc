from rest_framework import serializers
from .models import company
from backend.authentication.serializers import UserSerializer


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Company.objects.create(user=user, **validated_data)
        return company
