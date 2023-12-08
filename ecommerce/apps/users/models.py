from typing import List
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from ecommerce.apps.users.managers import CustomUserManager
from django.db import models


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = CustomUserManager()  # type: ignore

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField(
        validators=[
            MinValueValidator(10000),
            MaxValueValidator(99999)
        ]
    )
    phone = models.CharField(max_length=20)
