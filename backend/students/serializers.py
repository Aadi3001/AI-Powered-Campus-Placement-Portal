from rest_framework import serializers
from .models import StudentProfile
from .models import Education
from .models import Skill
from .models import Project
from .models import Internship
from .models import Certification


MAX_RESUME_BYTES = 5 * 1024 * 1024  # 5 MB


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'full_name', 'phone_number', 'date_of_birth',
            'degree', 'branch', 'graduation_year', 'cgpa',
            'resume', 'resume_text', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'resume_text', 'created_at', 'updated_at']

    def validate_resume(self, file):
        if file is None:
            return file
        if file.size > MAX_RESUME_BYTES:
            raise serializers.ValidationError('The file is too large (maximum 5 MB).')
        header = file.read(5)
        file.seek(0)
        if header != b'%PDF-':
            raise serializers.ValidationError('Please upload a valid PDF file.')
        return file

    def update(self, instance, validated_data):
        if 'resume' in validated_data:
            # A new resume was uploaded: clear the old text so it is read again
            instance.resume_text = ''
        return super().update(instance, validated_data)


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