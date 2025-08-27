from django.contrib import admin
from .models import Milestone

# Register your models here.
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "due_date", "progress")
    search_fields = ("name", "project__name")
    list_filter = ("project", "due_date")

admin.site.register(Milestone, MilestoneAdmin)