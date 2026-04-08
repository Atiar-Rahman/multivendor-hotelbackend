from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from users.models import User, GuestProfile, VendorAdminProfile, VendorStaffProfile


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','password','first_name','last_name']


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = ['phone']

class VendorAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAdminProfile
        fields = ['phone', 'vendor']

class VendorStaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorStaffProfile
        fields = ['vendor', 'designation']

# meserializer for meviewset
class MeSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'profile']
        read_only_fields = ['email']

    def get_profile(self, obj):
        if obj.role == User.Role.GUEST and hasattr(obj, 'guest_profile'):
            return GuestProfileSerializer(obj.guest_profile).data

        elif obj.role == User.Role.VENDOR_ADMIN and hasattr(obj, 'vendor_admin_profile'):
            return VendorAdminProfileSerializer(obj.vendor_admin_profile).data

        elif obj.role == User.Role.VENDOR_STAFF and hasattr(obj, 'vendor_staff_profile'):
            return VendorStaffProfileSerializer(obj.vendor_staff_profile).data

        return None
    


class UserSerializer(serializers.ModelSerializer):
    guest_profile = GuestProfileSerializer(read_only=True)
    vendor_admin_profile = VendorAdminProfileSerializer(read_only=True)
    vendor_staff_profile = VendorStaffProfileSerializer(read_only=True)

    class Meta:
        ref_name='customuser'
        model = User
        fields = ['id', 'email', 'role', 'guest_profile', 'vendor_admin_profile', 'vendor_staff_profile']
        read_only_fields = ['id','email']




class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','role']
        read_only_fields = ['email']

    def validate_role(self, value):
        requester = self.context.get('request').user  # user making the request
        user_to_update = self.instance  # user whose role is being changed

        # Prevent changing own role
        if user_to_update.id == requester.id:
            raise serializers.ValidationError("You cannot change your own role.")

        # SUPER_ADMIN can do anything
        if requester.role == User.Role.SUPER_ADMIN:
            return value

        # VENDOR_ADMIN restrictions
        if requester.role == User.Role.VENDOR_ADMIN:
            # Cannot assign SUPER_ADMIN
            if value == User.Role.SUPER_ADMIN:
                raise serializers.ValidationError("Vendor admins cannot assign SUPER_ADMIN role.")

            # Cannot change own role
            if user_to_update.id == requester.id:
                raise serializers.ValidationError("You cannot change your own role.")

            # Otherwise allowed
            return value

        # Other roles cannot change roles
        raise serializers.ValidationError("You do not have permission to change roles.")