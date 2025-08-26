# Import necessary modules from Django and our CustomUser model.
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# Form for creating a new user (e.g., on a sign-up page or in the admin).
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # Tell the form which model it's associated with.
        model = CustomUser

        # Specify the fields to display on the form.
        # Password fields are included by default in UserCreationForm.
        fields = ("email",)


# Form for updating an existing user's information.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        # Tell the form which model it's associated with.
        model = CustomUser

        # Specify the fields to display. You can show any fields from your CustomUser model.
        # The password field is intentionally left out here to prevent accidental changes.
        fields = ("email",)
