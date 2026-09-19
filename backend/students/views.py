from rest_framework import generics, permissions
from .models import StudentProfile, Education, Skill
from .serializers import StudentProfileSerializer, EducationSerializer, SkillSerializer


class MyStudentProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  -> returns the logged-in student's own profile
    PUT/PATCH -> updates the logged-in student's own profile
    Profile must already exist (created separately, see Step 9d).
    """
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the profile belonging to the current logged-in user
        return self.request.user.student_profile


class EducationListCreateView(generics.ListCreateAPIView):
    """
    GET  -> list all education entries for the logged-in student
    POST -> add a new education entry for the logged-in student
    """
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return education entries belonging to the logged-in user
        return Education.objects.filter(student=self.request.user.student_profile)

    def perform_create(self, serializer):
        # Automatically attach the logged-in user's profile as the owner
        serializer.save(student=self.request.user.student_profile)


class SkillListCreateView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(student=self.request.user.student_profile)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)