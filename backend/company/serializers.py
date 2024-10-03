from rest_framework import serializers
from .models import Company
from authentication.serializers import UserSerializer
from authentication.models import User

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        company = Company.objects.create(user=user, **validated_data)
        return company
