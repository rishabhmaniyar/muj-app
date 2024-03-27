from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    key = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(null=True)
