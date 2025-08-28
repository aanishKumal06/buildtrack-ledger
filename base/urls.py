from django.urls import path

from .views import HomeView, ReportView

urlpatterns = [
    path('report/', ReportView.as_view(), name='project_report'),
    path("", HomeView.as_view(), name="home"),
]
