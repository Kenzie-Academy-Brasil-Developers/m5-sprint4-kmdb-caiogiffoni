from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birthdate = models.DateField()
    bio = models.TextField(blank=True, null=True)
    is_critic = models.BooleanField(default=False)
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # campos pedidos no TERMINAL com createsuperuser
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "birthdate"]
