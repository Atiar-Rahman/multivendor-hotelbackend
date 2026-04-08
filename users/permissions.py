from rest_framework import permissions
from users.models import User

class IsSuperAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user.is_authenticated
        return request.user.role == User.Role.SUPER_ADMIN
    



class IsUpperLevelRestricted(permissions.BasePermission):
    """
    Prevent users from accessing users above their role.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # SUPER_ADMIN can do anything
        if user.role == 'super_admin':
            return True

        # VENDOR_ADMIN cannot access SUPER_ADMIN
        if user.role == 'vendor_admin' and obj.role == 'super_admin':
            return False

        # VENDOR_STAFF cannot access admin or above
        if user.role == 'vendor_staff' and obj.role in ['super_admin', 'vendor_admin']:
            return False

        # Everyone else can access their own or lower
        return True