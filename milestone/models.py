from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from base.models import AbstractBaseModel
from project.models import Project  

class Milestone(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="milestones")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    due_date = models.DateField()
    progress = models.PositiveIntegerField(default=0)  # % complete

    def clean(self):
        # Ensure progress is between 0 and 100
        if not (0 <= self.progress <= 100):
            raise ValidationError({'progress': 'Progress must be between 0 and 100.'})

        # Ensure due_date is not after the project's end_date
        if self.project.end_date and self.due_date > self.project.end_date:
            raise ValidationError({'due_date': 'Due date cannot be after the project end date.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.progress}%)"
