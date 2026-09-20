from rest_framework import serializers
from .models import Company
from .models import RecruiterProfile
from .models import SkillTag
from .models import Job


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'industry', 'description', 'logo']


class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = ['id', 'company', 'full_name', 'designation', 'phone_number']


class SkillTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTag
        fields = ['id', 'name']


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'required_skills',
            'min_cgpa', 'eligible_branches', 'min_graduation_year',
            'max_graduation_year', 'location', 'salary_range',
            'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
