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

class UserSerializer(serializers.ModelSerializer):
    guest_profile = GuestProfileSerializer(read_only=True)
    vendor_admin_profile = VendorAdminProfileSerializer(read_only=True)
    vendor_staff_profile = VendorStaffProfileSerializer(read_only=True)

    class Meta:
        ref_name='customuser'
        model = User
        fields = ['id', 'email', 'role', 'guest_profile', 'vendor_admin_profile', 'vendor_staff_profile']
        read_only_fields = ['id']

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']

    def validate_role(self, value):
        request = self.context.get('request')
        if request and not request.user.role == User.Role.SUPER_ADMIN:
            raise serializers.ValidationError("Only super admins can change roles.")
        return value






