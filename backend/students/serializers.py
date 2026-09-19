from rest_framework import serializers
from .models import StudentProfile
from .models import Education
from .models import Skill


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'full_name', 'phone_number', 'date_of_birth',
            'degree', 'branch', 'graduation_year', 'cgpa',
            'resume', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'level', 'institution', 'board_or_university',
            'percentage_or_cgpa', 'year_of_completion',
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency']