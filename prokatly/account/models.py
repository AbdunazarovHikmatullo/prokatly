from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='account/avatar/%Y/%d/', null=True, blank=True)
    phone_number = models.CharField(max_length=9)
    
    def __str__(self):
        return f"{self.username} - {self.phone_number}"
    
