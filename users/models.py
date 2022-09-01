from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=120)
    email = models.EmailField(max_length=150)
    is_company = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name", "is_company"]