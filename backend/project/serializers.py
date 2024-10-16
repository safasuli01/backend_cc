from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    author_profile_image = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_field = ['author']

    def create(self, validated_data):
        # Automatically assign the logged-in user as the author
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            user = request.user
            if user.is_authenticated and hasattr(user, 'individual'):
                validated_data['author'] = user.individual  # Assign the authenticated user's individual profile
            else:
                raise serializers.ValidationError('User must be logged in and have an associated individual profile.')
        else:
            raise serializers.ValidationError('Request must include a user.')
        
        return super().create(validated_data)

    def get_author_username(self, obj):
        return obj.author.user.first_name if obj.author and obj.author.user else None  # Access the user's first name through author
    
    def get_author_profile_image(self, obj):
        return obj.author.profile_image.url if obj.author and obj.author.profile_image else None  # Access profile image URL