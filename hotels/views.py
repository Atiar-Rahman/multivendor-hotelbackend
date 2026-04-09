from rest_framework import viewsets, permissions
from hotels.models import Vendor,Contact
from hotels.serializers import VendorSerializer,VendorApproveSerializer,ContactSerializer
from hotels.permissions import VendorPermission
from datetime import timezone
from rest_framework.exceptions import PermissionDenied

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Any user can see approved vendors
        queryset = Vendor.objects.filter(is_approved=True)

        if user.role == 'super_admin':
            queryset = Vendor.objects.all()

        # Authenticated users can see their own vendors (approved or unapproved)
        if user.is_authenticated:
            queryset = queryset | Vendor.objects.filter(owner=user)
        
        return queryset

    def perform_create(self, serializer):
        # The current authenticated user is set as the owner of the new vendor
        serializer.save(owner=self.request.user)



class VendorApproveViewSet(viewsets.ModelViewSet):
    """
    Only super_admin can approve vendors
    """
    queryset = Vendor.objects.filter(is_approved=False)
    serializer_class = VendorApproveSerializer
    permission_classes = [permissions.IsAuthenticated,VendorPermission]

    def get_queryset(self):
        """
        Only super_admin can access unapproved vendors
        """
        user = self.request.user
        
        if user.role == 'super_admin':
            return Vendor.objects.filter(is_approved=False)
        return Vendor.objects.none()  # Others cannot see unapproved vendors

    def get_serializer_context(self):
        """
        Add current user to context so that it can be used in the serializer
        """
        context = super().get_serializer_context()
        context['request_user'] = self.request.user  # pass user context to serializer
        context['vendor_id'] = self.kwargs.get('vendor_pk')
        return context




class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.active_objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user =self.request.user)