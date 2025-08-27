from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from unfold.admin import ModelAdmin


# Define the admin class for the CustomUser model.
class CustomUserAdmin(ModelAdmin, UserAdmin):
    # The form used for creating a new user in the admin.
    add_form = CustomUserCreationForm

    # The form used for changing an existing user in the admin.
    form = CustomUserChangeForm

    # The model this admin class is for.
    model = CustomUser

    # The columns to display in the admin list view.
    list_display = [
        "email",
        "first_name",
        "is_staff",
    ]

    # The fields to display when editing a user. Organized into sections (fieldsets).
    # This overrides the default fieldsets which include 'username'.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal Information"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),

        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Modify the second fieldset

    # The fields to display when adding a new user.
    # 'password2' is for the confirmation field.
    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)

    # The field to use for ordering the list view.
    ordering = ["email"]


# Register your custom model and its admin class with the admin site.
admin.site.register(CustomUser, CustomUserAdmin)