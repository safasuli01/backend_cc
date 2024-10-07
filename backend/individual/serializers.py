# from rest_framework import serializers
# from .models import Individual
# from authentication.serializers import UserSerializer
# from authentication.models import User
#
# class IndividualSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#
#     class Meta:
#         model = Individual
#         fields = ['user', 'date_of_birth', 'gender', 'phone_number', 'specialization', 'national_id', 'account_type']
#
#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user_serializer = UserSerializer(data=user_data)
#         user_serializer.is_valid(raise_exception=True)
#         user = user_serializer.save()  # Create and save the User object
#
#         individual = Individual.objects.create(user=user, **validated_data)
#         return individual

from rest_framework import serializers
from .models import Individual
from authentication.serializers import UserSerializer


# class IndividualSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=False)  # Keep the user field optional

#     class Meta:
#         model = Individual
#         fields = '__all__'  # Ensure all fields are included

#     def create(self, validated_data):
#         user_data = validated_data.pop('user', None)  # Use a default of None
#         user = None
#         if user_data:  # Check if user_data is provided
#             user_serializer = UserSerializer(data=user_data)
#             user_serializer.is_valid(raise_exception=True)  # This will raise an error if invalid
#             user = user_serializer.save()  # Save the user only if valid
#         print(validated_data)
#         # Create an Individual object, handling the case where user is None
#         individual = Individual.objects.create(user=user, **validated_data)
#         return individual

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user_serializer = UserSerializer(data=user_data)
    #     user_serializer.is_valid(raise_exception=True)
    #     user = user_serializer.save()
    #     individual = Individual.objects.create(user=user, **validated_data)
    #     return individual




class IndividualSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)  # Set user as required

    class Meta:
        model = Individual
        fields = ['user', 'date_of_birth', 'gender', 'specialization', 
                  'national_id', 'account_type', 'phone_number', 'user']  # Explicitly include fields

    def create(self, validated_data):
        # Extract user data from the validated_data
        user_data = validated_data.pop('user')
        
        # Create a user instance using the UserSerializer
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Now, create the Individual object and associate the user
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
