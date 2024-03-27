from django.db import models



class Login(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
