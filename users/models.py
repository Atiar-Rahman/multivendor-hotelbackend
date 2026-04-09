from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from core.models import SoftDeleteModel
# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin'
        VENDOR_ADMIN = 'vendor_admin'
        VENDOR_STAFF =  'vendor_staff'
        GUEST = 'guest'
    
    username=None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.GUEST)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

# role based profile created
class GuestProfile(SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guest_profile')
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    def __str__(self):
        return f'Guest: {self.user.email}'
    
class VendorAdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_admin_profile')
    phone=models.CharField(max_length=20,blank=True,null=True)
    vendor = models.ForeignKey('hotels.Vendor', on_delete=models.CASCADE, null=True, blank=True,related_name='admins')

    def __str__(self):
        return f'Vendor admin: {self.user.email}'


class VendorStaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_staff_profile")
    vendor = models.ForeignKey("hotels.Vendor", on_delete=models.CASCADE,null=True,blank=True, related_name="staff")
    designation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Staff: {self.user.email}"
    
