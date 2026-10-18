from rest_framework.permissions import SAFE_METHODS, BasePermission


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


class IsRecruiterOrReadOnly(BasePermission):
    """Any logged-in user may read; only recruiters may create or change."""
    message = 'Only recruiters can make changes here.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.role == 'RECRUITER'