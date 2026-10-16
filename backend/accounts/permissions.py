from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    message = 'Only students can access this.'

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == 'STUDENT')


class IsRecruiter(BasePermission):
    message = 'Only recruiters can access this.'

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == 'RECRUITER')