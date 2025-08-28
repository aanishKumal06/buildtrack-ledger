from django.db import models
from datetime import date
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from base.models import AbstractBaseModel

# Create your models here.
class ProjectStatus(models.TextChoices):
    PLANNING = "PLANNING", "Planning"
    ACTIVE = "ACTIVE", "Active"
    ON_HOLD = "ON_HOLD", "On Hold"
    COMPLETE = "COMPLETE", "Complete"
    CANCELLED = "CANCELLED", "Cancelled"

class Role(models.TextChoices):
    PROJECT_MANAGER = "PROJECT_MANAGER", "Project Manager"
    TEAM_MEMBER = "TEAM_MEMBER", "Team Member"

class Project(AbstractBaseModel):
    name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PLANNING)
    description = models.TextField(blank=True)
    actual_cost  = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"{self.name} - {self.status}"

    @property
    def overall_progress(self):
        milestones = self.milestones.all()
        if not milestones.exists():
            return 0
        total = sum(m.progress for m in milestones)
        return round(total / milestones.count())

    @property
    def total_income(self):
        return sum((income.amount for income in self.incomes.all()), Decimal("0.00"))

    @property
    def total_expense(self):
        return sum((exp.amount for exp in self.expenses.all()), Decimal("0.00"))

    @property
    def profit_loss(self):
        return self.total_income - self.total_expense

    @property
    def variance(self):
        return self.actual_cost  - self.total_expense

    def clean(self):
        # Validate start_date <= end_date
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError({'start_date': 'Start date cannot be after end date.'})

        # Prevent start date in the past
        if self.start_date < date.today():
            raise ValidationError({'start_date': 'Start date cannot be in the past.'})

    def save(self, *args, **kwargs):
        self.clean()  # validate before saving
        super().save(*args, **kwargs)

class ProjectMember(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.TEAM_MEMBER)

    def __str__(self):
        return f"{self.user} {self.role} {self.project}"

    def clean(self):
        # Check if there is already a Project Manager for this project
        if self.role == Role.PROJECT_MANAGER:
            existing_pm = ProjectMember.objects.filter(
                project=self.project, role=Role.PROJECT_MANAGER
            )
            # Exclude self if updating existing record
            if self.pk:
                existing_pm = existing_pm.exclude(pk=self.pk)
            if existing_pm.exists():
                raise ValidationError("This project already has a Project Manager.")

    def save(self, *args, **kwargs):
        self.clean()  # validate before saving
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["project", "user"], name="unique_project_member")
        ]

