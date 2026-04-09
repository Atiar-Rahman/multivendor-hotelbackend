from django.db import models
from django.contrib.auth import get_user_model
from core.models import SoftDeleteModel

User = get_user_model()

# Create your models here.
# Vendor model 
class Vendor(SoftDeleteModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'vendor_admin'})
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.owner.email})"
    



class Contact(SoftDeleteModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    vendor_id = models.CharField(max_length=50)
    comments = models.TextField()


    def __str__(self):
        return self.user.email 
    

