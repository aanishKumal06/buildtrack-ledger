from django.urls import path

from .views import MilestoneCreateView, MilestoneListView, MilestoneIdView, MilestoneUpdateView, MilestoneDeleteView

urlpatterns = [
    path("milestone/", MilestoneListView.as_view(), name="milestone_list"),
    path("milestone/<int:project_id>/", MilestoneIdView.as_view(), name="milestone_list_by_project"),
    path("milestone/create/", MilestoneCreateView.as_view(), name="milestone_create"),
    path("milestone/<int:milestone_pk>/update/", MilestoneUpdateView.as_view(), name="milestone_update"),
    path("milestone/<int:milestone_pk>/delete/", MilestoneDeleteView.as_view(), name="milestone_delete"),
]
