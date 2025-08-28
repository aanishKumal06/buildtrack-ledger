from django.views import View
from django.shortcuts import render, redirect
from .models import Project, ProjectMember, Role
from .forms import ProjectForm, ProjectMemberForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# from milestones.models import Milestone


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ProjectAccessMixin(UserPassesTestMixin):
    def test_func(self):
        project_pk = self.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_pk)

        membership = ProjectMember.objects.filter(
            project=project,
            user=self.request.user
        ).first()
        print(membership)
        # Only allow if user is project manager
        return self.request.user.is_staff or membership.role == Role.PROJECT_MANAGER


class ProjectListView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user

        if user.is_staff:
            # Staff sees all projects
            projects = Project.objects.all().prefetch_related( "members__user")
        else:
            # Regular users see only projects assigned to them
            projects = Project.objects.filter(
                members__user_id=user.id  # use user.id here
            ).prefetch_related("milestones", "members__user")

        return render(request, "project/project_list.html", {"projects": projects})

class ProjectCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request):
        template_name = "project/form.html"
        context = {
            "form": ProjectForm(),
            "button_label": "Create Project"
        }
        return render(request, template_name, context)

    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project created successfully!")
            return redirect("project_list") 
        else:
            messages.error(request, "Please correct the errors below.")
            template_name = "project/form.html"
            context = {"form": form}
            return render(request, template_name, context)

class ProjectMemberCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request):
        template_name = "project/form.html"
        context = {
            "form": ProjectMemberForm(),
            "button_label": "Add Project Member"
        }
        return render(request, template_name, context)

    def post(self, request):
        form = ProjectMemberForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, "Project member added successfully!")
            form.save()
            return redirect("project_list") 
        else:
            messages.error(request, "Could not add member. Please check the form.")
            template_name = "project/form.html"
            context = {"form": form}
            return render(request, template_name, context)


class ProjectUpdateView(LoginRequiredMixin, ProjectAccessMixin,  View):
    def get(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        template_name = "project/form.html"
        context = {
            "form": ProjectForm(instance=project),
            "button_label": "Update Project"
        }
        return render(request, template_name, context)

    def post(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("project_list")
        else:
            messages.error(request, "Update failed. Please fix the errors.")
            template_name = "project/form.html"
            context = {
                "form": form,
                "button_label": "Update Project"
            }
            return render(request, template_name, context)

class ProjectDeleteView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        template_name = "project/delete.html"
        context = {"project": project}
        return render(request, template_name, context)

    def post(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("project_list")

class ProjectDetailView(LoginRequiredMixin, View):
    def get(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        template_name = "project/project_details.html"
        context = {"project": project}
        return render(request, template_name, context)

class ProjectMemberUpdateView(LoginRequiredMixin, ProjectAccessMixin, View):
    def get(self, request, project_pk, member_pk):
        
        member = ProjectMember.objects.get(pk=member_pk)
        template_name = "project/form.html"
        context = {
            "form": ProjectMemberForm(instance=member),
            "button_label": "Update Project Member"
        }
        return render(request, template_name, context)

    def post(self, request, project_pk, member_pk):
        member = ProjectMember.objects.get(pk=member_pk)
        form = ProjectMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Project member updated successfully!")
            return redirect("project_detail", project_pk=project_pk)
        else:
            messages.error(request, "Update failed. Please fix the errors.")
            template_name = "project/form.html"
            context = {
                "form": form,
                "button_label": "Update Project Member"
            }
            return render(request, template_name, context)


