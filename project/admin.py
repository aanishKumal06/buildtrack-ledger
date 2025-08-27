from django.contrib import admin
from .models import Project, ProjectMember

# Register your models here.
admin.site.site_header = "Project Management Admin"
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "client_name", "start_date", "end_date", "status", "actual_cost")
    search_fields = ("name", "client_name")
    list_filter = ("status", "start_date", "end_date")

admin.site.register(Project, ProjectAdmin)

class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "role")
    search_fields = ("user__username", "project__name", "role")
    list_filter = ("project", "role")

admin.site.register(ProjectMember, ProjectMemberAdmin)

