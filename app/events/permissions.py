from rest_framework.permissions import BasePermission

class IsAlumniOrStudent(BasePermission):
    def has_permission(self, request, view):
        # Assuming you have a user model with a role attribute
        return request.user.is_authenticated and (request.user.role in ['alumni', 'student'])