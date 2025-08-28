from django.urls import path

from .views import ProjectListView, ProjectCreateView, ProjectMemberCreateView, ProjectUpdateView, ProjectDeleteView, ProjectDetailView

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="project_list"),
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path("projects/members/create/", ProjectMemberCreateView.as_view(), name="project_member_create"),
    path("projects/<int:project_pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:project_pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("projects/<int:project_pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
