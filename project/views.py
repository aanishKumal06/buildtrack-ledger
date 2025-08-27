from django.views import View
from django.shortcuts import render
from .models import Project


class ProjectListView(View):
    def get(self, request):
        user = request.user

        if user.is_staff:
            # Staff sees all projects
            projects = Project.objects.all()
        else:
            # Regular users see only projects assigned to them
            projects = Project.objects.filter(
                members__user_id=user.id  # use user.id here
            )

        return render(request, "project/project_list.html", {"projects": projects})
