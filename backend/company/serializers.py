from rest_framework import serializers
from .models import Company
from authentication.serializers import UserSerializer
from authentication.models import User

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # Make user field optional

    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {
            'registration_documents': {'required': False},
            'logo': {'required': False},
        }
        

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'company'
        user = User.objects.create_user(**user_data)
        
        company = Company.objects.create(user=user, **validated_data)
            
        return company
    