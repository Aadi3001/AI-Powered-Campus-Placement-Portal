from rest_framework import serializers
from .models import User


SELF_REGISTER_ROLES = ['STUDENT', 'RECRUITER']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Validates registration input and creates a new User.
    Password is write-only so it never appears in API responses.
    """
    
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        # use create_user (not create) so the password gets hashed properly
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
        )
        return user

    def validate_role(self, value):
        if value not in SELF_REGISTER_ROLES:
            raise serializers.ValidationError(
                'You can only register as a student or a recruiter.'
            )
        return value