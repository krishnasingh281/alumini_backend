from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Allow access only to Admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsAlumniUser(BasePermission):
    """Allow access only to Alumni users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "alumni"

class IsStudentUser(BasePermission):
    """Allow access only to Students."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"
