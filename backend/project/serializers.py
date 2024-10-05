from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    # class Meta:
    #     model = Project
    #     fields = ['id', 'title', 'description', 'industry', 'author', 'post_status', 'created_at', 'deadline',
    #               'budget']
    #     read_only_fields = ['created_at']

    # def create(self, validated_data):
    #     if 'author' not in validated_data:
    #         raise ValueError("Author must be provided.")  
    #     # Create the project instance with the provided data
    #     job = Project.objects.create(**validated_data)

    #     return project

    # def update(self, instance, validated_data):
    #     # Update fields of the Job instance with validated data, fallback to existing data if not provided
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.industry = validated_data.get('industry', instance.industry)
    #     instance.budget = validated_data.get('budget', instance.budget)
    #     instance.deadline = validated_data.get('job_type', instance.deadline)

    #     # Only update author if it's provided (optional)
    #     if 'author' in validated_data:
    #         instance.author = validated_data['author']

    #     # Update post status if provided
    #     if 'post_status' in validated_data:
    #         instance.post_status = validated_data['post_status']

    #     # Save the updated instance
    #     instance.save()
    #     return instance
