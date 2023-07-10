from django.db import models
from django.contrib.auth.models import AbstractUser, Group


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group)
    # username = None

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
