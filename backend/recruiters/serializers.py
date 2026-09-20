from rest_framework import serializers
from .models import Company
from .models import RecruiterProfile


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'industry', 'description', 'logo']


class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = ['id', 'company', 'full_name', 'designation', 'phone_number']

