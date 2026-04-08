from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users.models import GuestProfile, VendorAdminProfile, VendorStaffProfile

User = get_user_model()

# auto-create profile on user creation

@receiver(post_save,sender=User)
def create_profile(sender,instance, created, **kwargs):
    if created:
        if instance.role == User.Role.GUEST:
            GuestProfile.objects.create(user=instance)
        elif instance.role == User.Role.VENDOR_ADMIN:
            VendorAdminProfile.objects.create(user=instance)
        elif instance.role == User.Role.VENDOR_STAFF:
            VendorStaffProfile.objects.create(user=instance, vendor=None)


#handle role change and profile change

@receiver(pre_save, sender=User)
def handle_role_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    previous = User.objects.get(pk=instance.pk)
    old_role = previous.role
    new_role = instance.role

    if old_role != new_role:
        # Delete old profile
        if old_role == User.Role.GUEST:
            GuestProfile.objects.filter(user=instance).delete()
        elif old_role == User.Role.VENDOR_ADMIN:
            VendorAdminProfile.objects.filter(user=instance).delete()
        elif old_role == User.Role.VENDOR_STAFF:
            VendorStaffProfile.objects.filter(user=instance).delete()

        # Create new profile
        if new_role == User.Role.GUEST:
            GuestProfile.objects.create(user=instance)
        elif new_role == User.Role.VENDOR_ADMIN:
            VendorAdminProfile.objects.create(user=instance, vendor=None)
        elif new_role == User.Role.VENDOR_STAFF:
            VendorStaffProfile.objects.create(user=instance, vendor=None)