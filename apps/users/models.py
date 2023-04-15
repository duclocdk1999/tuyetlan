from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email           = models.EmailField(unique=True, null=False, blank=False, max_length=200)
    name            = models.CharField(max_length=200)

    EMAIL_FIELD     = "email"
    REQUIRED_FIELDS = ["email", "name", "password"]

    def __str__(self):
        return f"{self.email} {self.name}"