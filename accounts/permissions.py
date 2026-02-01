from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admin users.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admin users.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can access everything
        if request.user.role == 'admin':
            return True
        
        # Users can only access their own objects
        return obj == request.user