from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserSerializer,GuestProfileSerializer,VendorAdminProfileSerializer,VendorStaffProfileSerializer
from users.permissions import IsSuperAdminOrReadOnly,IsUpperLevelRestricted
from rest_framework.response import Response
from .serializers import MeSerializer
from django.db import models


class MeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

    def partial_update(self, request):
        user = request.user

        # profile update logic
        if user.role == "guest":
            profile = user.guest_profile
            serializer = GuestProfileSerializer(profile, data=request.data, partial=True)

        elif user.role == "vendor_admin":
            profile = user.vendor_admin_profile
            serializer = VendorAdminProfileSerializer(profile, data=request.data, partial=True)

        elif user.role == "vendor_staff":
            profile = user.vendor_staff_profile
            serializer = VendorStaffProfileSerializer(profile, data=request.data, partial=True)

        else:
            return Response({"error": "Invalid role"}, status=400)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly, IsUpperLevelRestricted]
    def get_queryset(self):
        
        # short circuit during swagger schema diagram
        if getattr(self, 'swagger_fake_view',False):
            return User.objects.none()
        
        user = self.request.user
        # SUPER_ADMIN → see all users
        if user.role == User.Role.SUPER_ADMIN:
            return User.objects.all()

        # VENDOR_ADMIN → see only their vendor's users
        elif user.role == User.Role.VENDOR_ADMIN:
            vendor = user.vendor_admin_profile.vendor
            return User.objects.filter(
                models.Q(vendor_admin_profile__vendor=vendor) | 
                models.Q(vendor_staff_profile__vendor=vendor) |
                models.Q(guest_profile__user__vendor_admin_profile__vendor=vendor)  # if guests tied to vendor
            )

        # VENDOR_STAFF → only same vendor users (downline only)
        elif user.role == User.Role.VENDOR_STAFF:
            vendor = user.vendor_staff_profile.vendor
            return User.objects.filter(
                models.Q(vendor_staff_profile__vendor=vendor) |
                models.Q(guest_profile__user__vendor_admin_profile__vendor=vendor)
            )

        # GUEST → only self
        return User.objects.filter(id=user.id)
    
