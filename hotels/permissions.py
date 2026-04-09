from rest_framework import permissions

class VendorPermission(permissions.BasePermission):
    """
    - vendor_admin: can only access their own approved vendors
    - super_admin: can access all vendors, approved or unapproved
    - others: can only view approved vendors (read-only)
    """

    def has_permission(self, request, view):
        # Only authenticated users can access any vendor
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # SAFE_METHODS: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            # super_admin can view all vendors
            if user.role == 'super_admin':
                return True
            # Others can only view approved vendors
            return obj.is_approved

        # Write permissions (POST, PUT, PATCH, DELETE)
        if user.role == 'super_admin':
            return True  # super_admin can modify any vendor

        if user.role == 'vendor_admin':
            # vendor_admin can modify only their own approved vendors
            return obj.is_approved and obj.owner == user

        # Others cannot write
        return False