from rest_framework import serializers
from hotels.models import Vendor,Contact
from django.utils import timezone

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id','owner','name','description','address','city','country','phone','email','logo','website','facebook','instagram','is_approved','approved_at','average_rating','review_count']
        read_only_fields = ['owner','is_approved', 'approved_at', 'average_rating', 'review_count']



class VendorApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'is_approved', 'approved_at']
        read_only_fields = ['id', 'approved_at']  # `approved_at` is auto-set and cannot be updated by users.

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # Check if the user is super_admin and trying to update is_approved
        if 'is_approved' in validated_data:
            if user.role != 'super_admin':
                raise serializers.ValidationError("Only super_admin can update the is_approved field.")
            
            # Automatically set approved_at when is_approved is set to True
            if validated_data['is_approved'] is True:
                instance.is_approved=True
                instance.approved_at = timezone.now()
            else:
                # Optional: if is_approved is set to False, you can clear approved_at
                instance.approved_at = None

        # Update the rest of the fields normally
        for field, value in validated_data.items():
            if field != 'is_approved':  # Don't override is_approved directly here
                setattr(instance, field, value)

        instance.save()
        return instance
       


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id','user','name','vendor_id','comments']
        read_only_fields = ['id','user']
