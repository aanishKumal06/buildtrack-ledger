from django.db import models
from django.contrib.auth.models import AbstractUser


from .managers import CustomUserManager
# Create your models here.

class roleChoices(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    PROJECT_MANAGER = "PROJECT_MANAGER", "Project Manager"
    TEAM_MEMBER = "TEAM_MEMBER", "Team Member"

class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This can be used to add additional fields or methods specific to the application.
    """

    # We set it to None to indicate we don't want to use it.
    username = None

    # This ensures that no two users can register with the same email.
    email = models.EmailField("email address", unique=True)
    role = models.CharField(
        max_length=30,
        choices=roleChoices.choices,
        default=roleChoices.TEAM_MEMBER,
    )

    # This tells Django to use the 'email' field for authentication instead of 'username'.
    USERNAME_FIELD = "email"

    # Define fields that are required when creating a user via the 'createsuperuser' command.
    # 'email' and 'password' are required by default.
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
