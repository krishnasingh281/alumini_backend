from rest_framework import permissions


class IsAdminOrAlumni(permissions.BasePermission):
    """
    Custom permission to only allow admin or alumni users to create/modify blog posts.
    Read operations are allowed for all users.
    """
    def has_permission(self, request, view):
        # Allow read operations (GET, HEAD, OPTIONS) for any user
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write operations only allowed for authenticated admin/alumni users
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'alumni']
        )


class IsCommentAuthor(permissions.BasePermission):
    """
    Custom permission to only allow the author of a comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the comment
        return obj.author == request.user


class IsPostAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    Read operations are allowed for any user.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read operations for any user
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions only for the post author
        return obj.author == request.user