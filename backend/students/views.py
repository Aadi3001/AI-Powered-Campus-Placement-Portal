from rest_framework import generics, permissions
from .models import StudentProfile
from .serializers import StudentProfileSerializer


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