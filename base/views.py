from django.views import View
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from project.models import Project, ProjectStatus

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        # Base queryset
        if user.is_staff:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(members__user_id=user.id)

        # Aggregate counts
        project_counts = projects.aggregate(
            total_count=Count('id'),
            planning_count=Count('id', filter=Q(status=ProjectStatus.PLANNING)),
            active_count=Count('id', filter=Q(status=ProjectStatus.ACTIVE)),
            on_hold_count=Count('id', filter=Q(status=ProjectStatus.ON_HOLD)),
            complete_count=Count('id', filter=Q(status=ProjectStatus.COMPLETE)),
            cancelled_count=Count('id', filter=Q(status=ProjectStatus.CANCELLED)),
        )

        # Prepare chart data
        chart_labels = ["Planning", "Active", "On Hold", "Complete", "Cancelled"]
        chart_data = [
            project_counts["planning_count"],
            project_counts["active_count"],
            project_counts["on_hold_count"],
            project_counts["complete_count"],
            project_counts["cancelled_count"],
        ]

        context = {
            "project_counts": project_counts,
            "chart_labels": chart_labels,
            "chart_data": chart_data,
        }

        return render(request, "base/home.html", context)

class ReportView(LoginRequiredMixin, View):
    def get(self, request):
        projects = Project.objects.all()

        total_income = sum([p.total_income for p in projects], Decimal("0.00"))
        total_expense = sum([p.total_expense for p in projects], Decimal("0.00"))
        total_profit = sum([p.profit_loss for p in projects], Decimal("0.00"))
        avg_progress = round(sum([p.overall_progress for p in projects])/projects.count(), 2) if projects.exists() else 0

        # Add is_profit property
        for p in projects:
            p.is_profit = p.profit_loss >= 0

        chart_labels = [p.name for p in projects]
        chart_data = [float(p.profit_loss) for p in projects]

        context = {
            "projects": projects,
            "total_income": total_income,
            "total_expense": total_expense,
            "total_profit": total_profit,
            "avg_progress": avg_progress,
            "chart_labels": chart_labels,
            "chart_data": chart_data,
        }

        return render(request, "base/report.html", context)