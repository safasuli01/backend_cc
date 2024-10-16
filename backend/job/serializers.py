from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['author']
    
    def get_author_username(self, obj):
        return obj.author.user.username if obj.author and obj.author.user else None # Access the user's first name through author


    def get_company_logo(self, obj):
        return obj.author.logo.url if obj.author and obj.author.logo else None




    # class Meta:
    #     model = Job
    #     fields = ['id', 'title', 'description']
    #             #   , 'industry', 'author', 'post_status', 'created_at', 'location',
    #             #   'job_type']
    #     read_only_fields = ['created_at']

    # def create(self, validated_data):
    #     if 'author' not in validated_data:
    #         raise ValueError("Author must be provided.")  # You can customize this exception if needed

    #     # Create the job instance with the provided data
    #     job = Job.objects.create(**validated_data)

    #     return job

    # def update(self, instance, validated_data):
    #     # Update fields of the Job instance with validated data, fallback to existing data if not provided
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.industry = validated_data.get('industry', instance.industry)
    #     instance.location = validated_data.get('location', instance.location)
    #     instance.job_type = validated_data.get('job_type', instance.job_type)

    #     # Only update author if it's provided (optional)
    #     if 'author' in validated_data:
    #         instance.author = validated_data['author']

    #     # Update post status if provided
    #     if 'post_status' in validated_data:
    #         instance.post_status = validated_data['post_status']

    #     # Save the updated instance
    #     instance.save()
    #     return instance
