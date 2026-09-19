from rest_framework import serializers
from .models import StudentProfile
from .models import Education
from .models import Skill
from .models import Project
from .models import Internship
from .models import Certification


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


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'technologies_used', 'project_link']


class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ['id', 'company_name', 'role', 'start_date', 'end_date', 'description']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'title', 'issuing_organization', 'issue_date', 'credential_url']