from django.db import models


# Create your models here.
class Credentials(models.Model):
    app_name = models.CharField(max_length=255, unique=True)
    app_source = models.CharField(max_length=255, null=True)
    user_id = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    user_key = models.CharField(max_length=255, null=True)
    encryption_key = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, null=True)