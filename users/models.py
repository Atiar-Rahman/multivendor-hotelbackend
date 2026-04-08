from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
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
