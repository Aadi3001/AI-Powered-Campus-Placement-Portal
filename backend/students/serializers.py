from rest_framework import serializers
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'full_name', 'phone_number', 'date_of_birth',
            'degree', 'branch', 'graduation_year', 'cgpa',
            'resume', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']