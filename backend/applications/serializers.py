from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'status', 'applied_at']
        read_only_fields = ['id', 'status', 'applied_at']
        

class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'status']
        read_only_fields = ['id']