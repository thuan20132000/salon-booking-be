from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"customer: {self.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.user:
            self.user = User.objects.create_user(username=self.phone_number, password=self.phone_number)
        super().save(*args, **kwargs)
    
    
    
    
    
    