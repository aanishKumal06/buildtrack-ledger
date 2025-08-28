from django.views import View
from django.shortcuts import render, redirect
from .models import Milestone
from .forms import MilestoneForm
from project.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class MilestoneListView(LoginRequiredMixin, View):
    def get(self, request):
        milestones = Milestone.objects.all()
        template_name = "milestone/milestone_list.html"
        context = {
            "milestones": milestones
        }
        return render(request, template_name, context)



class MilestoneIdView(LoginRequiredMixin, View):
    def get(self, request, project_id):
        template_name = "milestone/milestone_list.html"
        project = Project.objects.get(pk=project_id)
        milestones = Milestone.objects.filter(project=project).order_by("due_date")
        context = {
            "milestones": milestones
        }
        return render(request, template_name, context) 


class MilestoneCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = MilestoneForm()
        template_name = "milestone/form.html"
        context = {
            "form": form,
            "button_label": "Create Milestone"
        }
        return render(request, template_name, context)

    def post(self, request):
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.user = request.user
            milestone.save()
            messages.success(request, "Milestone created successfully!")
            return redirect("milestone_list")
        else:
            messages.error(request, "Please correct the errors below.")
            template_name = "milestone/form.html"
            context = {"form": form}
            return render(request, template_name, context)



class MilestoneUpdateView(LoginRequiredMixin, View):
    def get(self, request, milestone_pk):
        milestone = Milestone.objects.get(pk=milestone_pk)
        form = MilestoneForm(instance=milestone)
        template_name = "milestone/form.html"
        context = {
            "form": form,
            "button_label": "Update Milestone"
        }
        return render(request, template_name, context)

    def post(self, request, milestone_pk):
        milestone = Milestone.objects.get(pk=milestone_pk)
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            form.save()
            messages.success(request, "Milestone updated successfully!")
            return redirect("milestone_list")
        else:
            messages.error(request, "Update failed. Please fix the errors.")
            template_name = "milestone/form.html"
            context = {
                "form": form,
                "button_label": "Update Milestone"
            }
            return render(request, template_name, context)



class MilestoneDeleteView(LoginRequiredMixin, View):
    def get(self, request, milestone_pk):
        milestone = Milestone.objects.get(pk=milestone_pk)
        template_name = "milestone/delete.html"
        context = {
            "milestone": milestone
        }
        return render(request, template_name, context)

    def post(self, request, milestone_pk):
        milestone = Milestone.objects.get(pk=milestone_pk)
        milestone.delete()
        messages.success(request, "Milestone deleted successfully!")
        return redirect("milestone_list")